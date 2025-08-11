#se traen todas las librerias necesarias
from filterpy.kalman import KalmanFilter
import algoritmos_busqueda as ab
import algoritmos_posicinamiento as ap
import osmnx as ox
import pandas as pd
import numpy as np
import os
import json
#import algoritmos_senales as algs
#from scipy.signal import filtfilt,firwin,lfilter,welch

#variables base - MODIFICADAS PARA RECWAY
import pathlib
base_path = pathlib.Path(__file__).parent.parent.parent
carpeta_csv = str(base_path / "uploads" / "csv" / "raw") #carpeta donde se encuentras los archivos csv que se van a cargar
prefijo_busqueda = "RecWay_"#prefijo que todo archivo a procesar debe contener 
carpeta_archivos_json = str(base_path / "uploads" / "json" / "output") #carpeta donde se generan los archivos json
carpeta_almacenamiento_csv = str(base_path / "uploads" / "csv" / "processed") #carpeta donde se almacenan los csv
carpeta_almacenamiento_json = str(base_path / "uploads" / "json" / "storage") #carpeta donde se almacenan los json

#clase con los datos de procesamiento 
class DatosProcesamiento:
    def __init__(self):
        # Variables globales o de contexto
        self.G = None
        self.latitud = None
        self.longitud = None
        self.numero_grafo = None
        self.G_exist = False
        self.carpeta_grafos = str(base_path / 'grafos_archivos5')
        self.L = 0.0003
        self.id_edge = None
        self.info_edge = None
        self.coordenadas_segmento = None
        self.coordenadas_subsegmento = None
        self.longitud_subsegmento = None
        self.posicion_subsegmento = None
        self.segmento_encontrado = False
        self.primera_muestra = False
        self.velocidad = None
        self.heading = None
        self.cambio_segmento = False #variable que indica cuando se cambio el segmento
        self.indice_subsegmento = 0
        self.segmento_maximo = 100
###############################################################
#-----------------SUB FUNCIONES MAIN -------------------------#

#se extraen los puntos GPS del mapa
def adquirir_latitud_longitud(datos,index_GPS):
    
    datos.latitud = df_gps['gps_lat'].iloc[index_GPS]
    datos.longitud = df_gps['gps_lng'].iloc[index_GPS]
    datos.velocidad = df_gps['gps_speed'].iloc[index_GPS]
    datos.heading = df_gps['gps_heading_filtrado'].iloc[index_GPS]

#1. se va a extraer el grafo donde se encuentra el punto, en caso de ya tenerlo no hacer nada
def procesamiento_mapa(datos):

    if datos.G_exist:
    
        #se comprueba si el archivo pertenece al grafo 
        if(not ap.confirmar_grafo(datos.latitud, datos.longitud, datos.numero_grafo,datos.carpeta_grafos)):
            
            datos.numero_grafo = ap.determinar_grafo(datos.latitud, datos.longitud)# se extrae el numero de grafo de la latitud y longitud
            if ap.confirmar_grafo(datos.latitud, datos.longitud, datos.numero_grafo,datos.carpeta_grafos):                
                
                #extraer el nombre de grafo del nombre
                grafo_nombre = ap.buscar_archivos_por_prefijo(datos.carpeta_grafos, 'segN' + str(datos.numero_grafo) + 'pos')
                #extraer el grafo del archivo 
                datos.G = ox.load_graphml(filepath=str(grafo_nombre)[2:-2])
    else:
        datos.numero_grafo = ap.determinar_grafo(datos.latitud, datos.longitud)# se extrae el numero de grafo de la latitud y longitud
        if ap.confirmar_grafo(datos.latitud, datos.longitud, datos.numero_grafo,datos.carpeta_grafos):#se comprueba si el grafo existe y tiene datos
    
            #extraer el nombre de grafo del nombre
            grafo_nombre = ap.buscar_archivos_por_prefijo(datos.carpeta_grafos, 'segN' + str(datos.numero_grafo) + 'pos')
            #extraer el grafo del archivo 
            datos.G = ox.load_graphml(filepath=str(grafo_nombre)[2:-2])
            datos.G_exist = True

def procesamiento_mapa_simple(datos):
    num_grafo = ap.determinar_grafo(datos.latitud, datos.longitud)
    if datos.numero_grafo != num_grafo:

        grafo_nombre = ap.buscar_archivos_por_prefijo(datos.carpeta_grafos, 'segN' + str(num_grafo) + 'pos')
        datos.numero_grafo = num_grafo
        datos.G = ox.load_graphml(filepath=str(grafo_nombre)[2:-2])
        datos.G_exist = True


def ubicar_muestra_grafo(datos):
    datos.segmento_encontrado = False
    try:
        if not datos.primera_muestra:
            datos.id_edge = ox.nearest_edges(datos.G, X=datos.longitud, Y=datos.latitud)
            datos.info_edge = datos.G.edges[datos.id_edge]
            datos.coordenadas_segmento = ap.obtener_coordenadas_segmento(datos.G,datos.id_edge,datos.info_edge)
            datos.primera_muestra = True
            datos.segmento_encontrado = True
            datos.cambio_segmento = True
        else:
            datos.coordenadas_segmento = ap.obtener_coordenadas_segmento(datos.G,datos.id_edge,datos.info_edge)
            poligono = ap.generar_poligono_segmento_lonlat(datos.coordenadas_segmento,datos.L)
            point_in_edge = ap.punto_en_poligono(poligono,datos.longitud,datos.latitud)
            if not point_in_edge:
                datos.cambio_segmento = True
                try:
                    segmentos_anexos = ap.caminos_hasta_distanciav2(datos.G,datos.id_edge[0],datos.id_edge[1],50)
                except Exception as e:
                    print('[UBICAR] Error obteniendo segmentos anexos:', e)
                    return
                try:
                    angulos_segmento_original = ap.obtener_angulos_edge(datos.G,datos.id_edge[0],datos.id_edge[1])
                except Exception as e:
                    print('[UBICAR] Error angulos segmento original:', e)
                    angulos_segmento_original = []
                posibilidades_segmento = []
                for i in range(1,len(segmentos_anexos)):
                    try:
                        angulos_segmento_encontrado = ap.obtener_angulos_edge(datos.G,segmentos_anexos[i][0],segmentos_anexos[i][1])
                    except Exception as e:
                        # saltar arista inválida
                        continue
                    try:
                        diferencia_angular = ap.diferencia_angular(datos.heading,angulos_segmento_encontrado[0])
                    except Exception:
                        diferencia_angular = 999
                    try:
                        segmento_prueba = ap.obtener_coordenadas_segmento(datos.G,segmentos_anexos[i],datos.G.edges[segmentos_anexos[i]])
                    except Exception:
                        continue
                    try:
                        distancia_segmento = ap.distancia_segmento(segmento_prueba,datos.longitud,datos.latitud)
                    except Exception:
                        distancia_segmento = 999999
                    try:
                        poligono_prueba = ap.generar_poligono_segmento_lonlat(segmento_prueba,datos.L)
                        point_in_edge_prueba = ap.punto_en_poligono(poligono_prueba,datos.longitud,datos.latitud)
                    except Exception:
                        point_in_edge_prueba = False
                    peso_area = 1 if point_in_edge_prueba else 0
                    try:
                        peso_total = peso_area * 0.7 + (1/(1+distancia_segmento)) * 0.15 + (1/(1+diferencia_angular)) * 0.15
                    except Exception:
                        peso_total = 0
                    posibilidades_segmento.append({
                        'segmento': segmentos_anexos[i],
                        'peso': peso_total,
                        'distancia': distancia_segmento,
                        'diferencia_angular': diferencia_angular,
                        'area': point_in_edge_prueba
                    })
                if posibilidades_segmento:
                    mejor = max(posibilidades_segmento, key=lambda x: x['peso'])
                    if mejor['peso'] > 0:  # criterio básico
                        datos.id_edge = mejor['segmento']
                        try:
                            datos.info_edge = datos.G.edges[datos.id_edge]
                            datos.coordenadas_segmento = ap.obtener_coordenadas_segmento(datos.G,datos.id_edge,datos.info_edge)
                            datos.segmento_encontrado = True
                        except Exception as e:
                            print('[UBICAR] No se pudo actualizar al nuevo segmento:', e)
                else:
                    datos.segmento_encontrado = False
    except Exception as e:
        print('[UBICAR] Excepción general:', e)
        # no relanzar para no detener pipeline

    #se guarda el registro del punto dentro del segmento

def colocar_puntos_grafo(datos):
    resultado = ap.proyectar_segmento(datos.coordenadas_segmento,datos.longitud,datos.latitud)
    return resultado

def segmentar_grafo(datos):
        
    #se comprueba si el segmento es superior a los 60 metros
    if(datos.info_edge['length'] > datos.segmento_maximo):

        #en caso que si se especifa las divisiones y el tamaño de esas divisiones
        cantidad_divisiones = int(datos.info_edge['length']/datos.segmento_maximo)
        
        posicion = 1

        #se determina el arreglo de distancia acumulada de los segmentos 
        distancia_acumulada = ap.distancia_euclidiana_acumulada(datos.coordenadas_segmento)

        datos.longitud_subsegmento = distancia_acumulada[-1]/(cantidad_divisiones+1)

        lista_total = []
        lista_base = []
        lista_base.append(datos.coordenadas_segmento[0])

        #se recorre todo el arreglo para separar el segmento en las partes 
        for i in range(1,len(distancia_acumulada)):

            if(distancia_acumulada[i] > datos.longitud_subsegmento * posicion):

                posicion_punto_medio = ap.punto_en_recta_geografica_simple(datos.coordenadas_segmento[i-1][0],datos.coordenadas_segmento[i-1][1],datos.coordenadas_segmento[i][0],datos.coordenadas_segmento[i][1],datos.longitud_subsegmento * posicion - distancia_acumulada[i-1],distancia_acumulada[i] - distancia_acumulada[i-1])
                lista_base.append(posicion_punto_medio)
                lista_total.append(lista_base)
                lista_base = []
                lista_base.append(posicion_punto_medio)
                lista_base.append(datos.coordenadas_segmento[i])
                posicion += 1

            else:
                lista_base.append(datos.coordenadas_segmento[i])

        lista_total.append(lista_base)
        #al final del ciclo se genero una lista llamada lista total donde en cada posicion se encuentra otra lista con los segmentos
        #cortados

        #ahora se recorre esa lista y se mira en cual parte se encuentra el punto analizado

        for i in range(len(lista_total)):
            
            poligono_sub = ap.generar_poligono_segmento_lonlat(lista_total[i],datos.L)
            point_in_edge_sub = ap.punto_en_poligono(poligono_sub,datos.longitud,datos.latitud)
            
            if point_in_edge_sub:
                datos.coordenadas_subsegmento = lista_total[i]
                datos.longitud_subsegmento = datos.longitud_subsegmento
                datos.posicion_subsegmento = i
                break

    else:
        #si el segmento no supera los 60 metros se realiza el hash de manera normal
        datos.coordenadas_subsegmento = datos.coordenadas_segmento
        datos.longitud_subsegmento = datos.info_edge['length']
        datos.posicion_subsegmento = 0

def procesar_archivo_csv(nombre_archivo):
    print(f"[PROC] procesar_archivo_csv -> {nombre_archivo}")
    """Función principal para procesar un archivo CSV individual"""
    
    # Variables globales
    global carpeta_csv, prefijo_busqueda, carpeta_archivos_json, carpeta_almacenamiento_csv, carpeta_almacenamiento_json
    global df_gps
    
    contador_json = 1 
    #se extrae la metadata del dispositivo y su dataframe de los datos
    df,metadatos =  ap.cargar_csv_con_metadatos(carpeta_csv,nombre_archivo)
    print(f"[PROC] Filas DF original: {len(df)}")
    df_gps = ap.eliminar_muestras_gps_duplicadas(df)
    print(f"[PROC] Filas tras eliminar duplicadas: {len(df_gps)}")
    df_gps = ap.ajustar_heading_y_filtrar(df_gps)
    print(f"[PROC] Filas tras ajustar heading: {len(df_gps)}")
    df_gps = ap.filtrar_muestras_por_velocidad(df_gps,3)
    print(f"[PROC] Filas tras filtrar velocidad >3: {len(df_gps)}")
    #recortes_velocidad = algs.encontrar_segmentos_continuos(df_gps.index.tolist())

    posicion_recorte_velocidad = 0
    indice_segmento_previo = 0
    indice_anterior = 0
    #se crea la estructura base para manejar el grafo
    datos_mapa = DatosProcesamiento()
    lista_recortes = []

    # Coeficientes del numerador (b) y denominador (a)
    #senal_pura_ax = df['acc_x'].to_numpy()
    #senal_pura_wy = df['gyro_y'].to_numpy()
    #senal_pura_az  = df['acc_z'].to_numpy()
    #senal_pura_wx = df['gyro_x'].to_numpy()

    #senal_wx = lfilter(filtro_6hz,1.0,senal_pura_wx)
    #senal_ax = lfilter(filtro_10hz,1.0,senal_pura_ax)
    #senal_ax = lfilter(filtro_pasaltos_1hz,1.0,senal_ax)
    #senal_az = lfilter(filtro_3hz,1.0,senal_pura_az)

    #df.to_csv('archivov2.csv', index=False)


    for i in range(len(df_gps)):
        
        adquirir_latitud_longitud(datos_mapa,i)
        
        procesamiento_mapa_simple(datos_mapa)
        ubicar_muestra_grafo(datos_mapa)
        segmentar_grafo(datos_mapa)


        hash_segmento = ap.hash_segmento(datos_mapa.id_edge[0],datos_mapa.id_edge[1],(datos_mapa.posicion_subsegmento*1000)+datos_mapa.id_edge[2])

        #se guarda la información en caso que se cambie el segmento
        if datos_mapa.cambio_segmento:
                
            # Marcar el segmento anterior como terminado
            if indice_anterior != 0:
                lista_recortes[len(lista_recortes)-1]["indice_final"] = i - 1

            # Agregar nuevo segmento
            nuevo_segmento = {
                "id": hash_segmento,
                "nombre": f"Segmento_{len(lista_recortes)}",
                "coordenadas_segmento": datos_mapa.coordenadas_subsegmento,
                "longitud_via": datos_mapa.longitud_subsegmento,
                "tipo_via": datos_mapa.info_edge.get('highway', 'unknown'),
                "indice_inicial": i,
                "indice_final": len(df_gps) - 1,  # Se actualizará después
                "tiempo": ap.timestamp_a_iso8601(df_gps['timestamp'].iloc[i])
            }
            lista_recortes.append(nuevo_segmento)
            datos_mapa.cambio_segmento = False

        indice_anterior = i
            
    #en lista recortes se va a encontrar todos los segmentos que se especificaron en el recorrido

    #ahora utilizando esa intersecciones para marcar los valores de los indices 

    #---------------------------------------------------------------------------#
    #-----------------AQUI SE PONE EL PROCESAMIENTO DE LOS ALGORITMOS-----------#


    #importante como esta es una versión prototipo para el sistema se tiene que tomar en cuenta que el recorte de velocidad
    #puede recortar segmentos tomar en cuenta para el sistema final.

    resultado_json = []
    for i in range(len(lista_recortes)):
        lista_geometria = []
        for j in range(len(lista_recortes[i]["coordenadas_segmento"])):
            punto_geometria = {
                "latitud": lista_recortes[i]["coordenadas_segmento"][j][0],
                "longitud": lista_recortes[i]["coordenadas_segmento"][j][1]
            }
            lista_geometria.append(punto_geometria)

        lista_huecos = []
        hueco1 = {
            "latitud":lista_geometria[0]["latitud"],
            "longitud":lista_geometria[0]["longitud"],
            "magnitud" : float(np.random.randint(0, 5000)/1000),
            "velocidad" : float(np.random.randint(0, 5000)/1000),
        }

        hueco2 = {
            "latitud":lista_geometria[-1]["latitud"],
            "longitud":lista_geometria[-1]["longitud"],
            "magnitud" : float(np.random.randint(0, 5000)/1000),
            "velocidad" : float(np.random.randint(0, 5000)/1000),
        }

        lista_huecos.append(hueco1)
        lista_huecos.append(hueco2)

        datos_obtenidos = {
            "numero" : i,
            "id" : lista_recortes[i]["id"],
            "nombre" : lista_recortes[i]["nombre"],
            "longitud" : lista_recortes[i]["longitud_via"],
            "tipo" : lista_recortes[i]["tipo_via"],
            "latitud_origen" : lista_geometria[0]["latitud"],
            "latitud_destino" : lista_geometria[-1]["latitud"],
            "longitud_origen" : lista_geometria[0]["longitud"],
            "longitud_destino" : lista_geometria[-1]["longitud"],
            "geometria" : lista_geometria,
            "fecha" : lista_recortes[i]["tiempo"],
            "IQR" : float(np.random.randint(0, 5000)/1000),
            "iri" : float(np.random.randint(0, 20000)/1000),
            "IRI_modificado" : float(np.random.randint(0, 5000)/1000),
            "az" : float(np.random.randint(0, 5000)/1000),
            "ax" : float(np.random.randint(0, 5000)/1000),
            "wx" : float(np.random.randint(0, 5000)/1000),
            "huecos" : lista_huecos
        }

        resultado_json.append(datos_obtenidos)

    if(len (resultado_json) > 0):
        print("guardando los datos")
        # Usar carpeta actual si está vacía
        if carpeta_archivos_json == "":
            carpeta = os.getcwd()
        else:
            carpeta = carpeta_archivos_json

        # Crear carpeta si no existe
        os.makedirs(carpeta, exist_ok=True)

        # Construir ruta del archivo
        ruta_archivo = os.path.join(carpeta, 'datos' + str(contador_json) + '.json')

        # Guardar el archivo
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(resultado_json, archivo, ensure_ascii=False, indent=2)

        # Usar carpeta actual si está vacía
        if carpeta_almacenamiento_json == "":
            carpeta = os.getcwd()
        else:
            carpeta = carpeta_almacenamiento_json

        # Crear carpeta si no existe
        os.makedirs(carpeta, exist_ok=True)

        # Construir ruta del archivo
        ruta_archivo = os.path.join(carpeta, 'datos' + nombre_archivo[:-4] + 'save.json')
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(resultado_json, archivo, ensure_ascii=False, indent=2)
        contador_json +=1

        ab.mover_archivo(carpeta_csv,carpeta_almacenamiento_csv,nombre_archivo)
        
    print(f"[PROC] Segmentos detectados: {len(lista_recortes)}")
    print(f"[PROC] Resultado JSON segmentos: {len(resultado_json)}")
    return resultado_json

###############################################################
#-----------------       MAIN        -------------------------#

def procesar_archivos_pendientes():
    print("[PROC] procesar_archivos_pendientes")
    """Función principal que procesa todos los archivos pendientes"""
    
    #se extrae la lista de los archivos que cumplen con las condiciones del prefijo
    listado_csv_encontrados = ab.buscar_archivos_por_nombre(carpeta_csv,prefijo_busqueda)
    print(f"[PROC] Archivos encontrados: {listado_csv_encontrados}")
    resultados = []
    
    #se recorren la lista que tiene todas las condiciones
    for dato in listado_csv_encontrados:
        print(f"[PROC] Procesando listado -> {dato}")
        try:
            resultado = procesar_archivo_csv(dato)
            resultados.append({
                "archivo": dato,
                "status": "success",
                "segmentos": len(resultado)
            })
        except Exception as e:
            resultados.append({
                "archivo": dato,
                "status": "error",
                "error": str(e)
            })
            
    return resultados
