#se traen todas las librerias necesarias
import numpy as np
import pandas as pd
import os
from filterpy.kalman import KalmanFilter  # noqa: F401 (no se usa aún pero se conserva como en original)
import osmnx as ox
import algoritmos_posicinamiento as ap
import algoritmos_busqueda as ab
import json
import pathlib

# Ajuste de rutas para integrarse al backend actual
base_path = pathlib.Path(__file__).parent.parent.parent
#carpetas adaptadas al esquema real de la app
carpeta_csv = str(base_path / 'uploads' / 'csv' / 'raw')  # carpeta donde se encuentran los archivos csv que se van a cargar
prefijo_busqueda = 'RecWay_'
carpeta_archivos_json = str(base_path / 'uploads' / 'json' / 'output')
carpeta_almacenamiento_csv = str(base_path / 'uploads' / 'csv' / 'processed')
carpeta_almacenamiento_json = str(base_path / 'uploads' / 'json' / 'storage')

#clase con los datos de procesamiento 
class DatosProcesamiento:
    def __init__(self):
        self.G = None
        self.latitud = None
        self.longitud = None
        self.numero_grafo = None
        self.G_exist = False
        # carpeta grafos ajustada
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
        self.cambio_segmento = False
        self.segmento_maximo = 60

#-----------------SUB FUNCIONES MAIN -------------------------#

def adquirir_latitud_longitud(datos,index_GPS):
    datos.latitud = df_gps['gps_lat'].iloc[index_GPS]
    datos.longitud = df_gps['gps_lng'].iloc[index_GPS]
    datos.velocidad = df_gps['gps_speed'].iloc[index_GPS]
    datos.heading = df_gps['gps_heading_filtrado'].iloc[index_GPS]

def procesamiento_mapa(datos):
    if datos.G_exist:
        if not ap.confirmar_grafo(datos.latitud, datos.longitud, datos.numero_grafo, datos.carpeta_grafos):
            datos.numero_grafo = ap.determinar_grafo(datos.latitud, datos.longitud)
            if ap.confirmar_grafo(datos.latitud, datos.longitud, datos.numero_grafo, datos.carpeta_grafos):
                grafo_nombre = ap.buscar_archivos_por_prefijo(datos.carpeta_grafos, 'segN' + str(datos.numero_grafo) + 'pos')
                datos.G = ox.load_graphml(filepath=str(grafo_nombre)[2:-2])
                datos.G_exist = True
    else:
        datos.numero_grafo = ap.determinar_grafo(datos.latitud, datos.longitud)
        if ap.confirmar_grafo(datos.latitud, datos.longitud, datos.numero_grafo, datos.carpeta_grafos):
            grafo_nombre = ap.buscar_archivos_por_prefijo(datos.carpeta_grafos, 'segN' + str(datos.numero_grafo) + 'pos')
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
    if not datos.primera_muestra:
        datos.id_edge = ox.nearest_edges(datos.G, X=datos.longitud, Y=datos.latitud)
        datos.info_edge = datos.G.edges[datos.id_edge]
        datos.coordenadas_segmento = ap.obtener_coordenadas_segmento(datos.G, datos.id_edge, datos.info_edge)
        datos.primera_muestra = True
        datos.segmento_encontrado = True
        datos.cambio_segmento = True
    else:
        datos.coordenadas_segmento = ap.obtener_coordenadas_segmento(datos.G, datos.id_edge, datos.info_edge)
        poligono = ap.generar_poligono_segmento_lonlat(datos.coordenadas_segmento, datos.L)
        point_in_edge = ap.punto_en_poligono(poligono, datos.longitud, datos.latitud)
        if not point_in_edge:
            datos.cambio_segmento = True
            segmentos_anexos = ap.caminos_hasta_distanciav2(datos.G, datos.id_edge[0], datos.id_edge[1], 50)
            angulos_segmento_original = ap.obtener_angulos_edge(datos.G, datos.id_edge[0], datos.id_edge[1])
            posibilidades_segmento = []
            for i in range(1, len(segmentos_anexos)):
                for j in range(len(segmentos_anexos[i])):
                    id_segmento = (segmentos_anexos[i][j][0], segmentos_anexos[i][j][1], 0)
                    info_segmento = datos.G.edges[id_segmento]
                    coordenadas_edge = ap.obtener_coordenadas_segmento(datos.G, id_segmento, info_segmento)
                    poligono2 = ap.generar_poligono_segmento_lonlat(coordenadas_edge, datos.L)
                    point_in_edge2 = ap.punto_en_poligono(poligono2, datos.longitud, datos.latitud)
                    if point_in_edge2:
                        datos.segmento_encontrado = True
                        registro = {
                            'nivel': i,
                            'id': id_segmento,
                            'info': info_segmento,
                            'coordenadas': coordenadas_edge,
                            'distancia': ap.distancia_segmento(coordenadas_edge, datos.longitud, datos.latitud),
                            'direccion': ap.obtener_angulos_edge(datos.G, id_segmento[0], id_segmento[1]),
                            'nodo_origen': segmentos_anexos[i][j][5]
                        }
                        posibilidades_segmento.append(registro)
            mayor_peso = 0
            if len(posibilidades_segmento) > 0:
                for i in range(len(posibilidades_segmento)):
                    peso_nivel = 1 / posibilidades_segmento[i]['nivel']
                    peso_distancia = 1 - (posibilidades_segmento[i]['distancia'] / 300)
                    if posibilidades_segmento[i]['nodo_origen']:
                        diferencia_angulo = ap.diferencia_angular(posibilidades_segmento[i]['direccion'][0], angulos_segmento_original[0])
                    else:
                        diferencia_angulo = ap.diferencia_angular(posibilidades_segmento[i]['direccion'][0], angulos_segmento_original[1])
                    peso_direccion = 1 - (diferencia_angulo / 180)
                    angulo_180 = ((posibilidades_segmento[i]['direccion'][0] + 180) % 360) - 180
                    peso_angulo = 1 - abs(angulo_180 - datos.heading) / 180
                    peso_final = 0.8 * peso_direccion + 0.3 * peso_nivel + 0.1 * peso_distancia + 0.6 * peso_angulo
                    if peso_final > mayor_peso:
                        mayor_peso = peso_final
                        datos.id_edge = posibilidades_segmento[i]['id']
                        datos.info_edge = posibilidades_segmento[i]['info']
                        datos.coordenadas_segmento = posibilidades_segmento[i]['coordenadas']
                        datos.segmento_encontrado = True
        else:
            datos.segmento_encontrado = True
            datos.cambio_segmento = False
        if not datos.segmento_encontrado:
            segmento = ox.nearest_edges(datos.G, X=datos.longitud, Y=datos.latitud)
            datos.id_edge = segmento
            datos.info_edge = datos.G.edges[datos.id_edge]
            datos.coordenadas_segmento = ap.obtener_coordenadas_segmento(datos.G, datos.id_edge, datos.info_edge)
            datos.primera_muestra = True
            datos.segmento_encontrado = True

def colocar_puntos_grafo(datos):
    return ap.proyectar_segmento(datos.coordenadas_segmento, datos.longitud, datos.latitud)

def segmentar_grafo(datos):
    if datos.cambio_segmento:
        if datos.info_edge['length'] > datos.segmento_maximo:
            cantidad_divisiones = int(datos.info_edge['length'] / datos.segmento_maximo)
            posicion = 1
            distancia_acumulada = ap.distancia_euclidiana_acumulada(datos.coordenadas_segmento)
            datos.longitud_subsegmento = distancia_acumulada[-1] / (cantidad_divisiones + 1)
            lista_total = []
            lista_base = [datos.coordenadas_segmento[0]]
            for i in range(1, len(distancia_acumulada)):
                punto_cortado = datos.coordenadas_segmento[i]
                while distancia_acumulada[i] > (datos.longitud_subsegmento * posicion):
                    longitud_faltante = (datos.longitud_subsegmento * posicion) - distancia_acumulada[i - 1]
                    punto_cortado = ap.punto_en_recta_geografica_simple(
                        datos.coordenadas_segmento[i - 1][1],
                        datos.coordenadas_segmento[i - 1][0],
                        datos.coordenadas_segmento[i][1],
                        datos.coordenadas_segmento[i][0],
                        longitud_faltante,
                        distancia_acumulada[i] - distancia_acumulada[i - 1]
                    )
                    lista_base.append(punto_cortado)
                    lista_total.append(lista_base)
                    lista_base = [punto_cortado]
                    punto_cortado = datos.coordenadas_segmento[i]
                    posicion += 1
                lista_base.append(punto_cortado)
            lista_total.append(lista_base)
            for i in range(len(lista_total)):
                poligono = ap.generar_poligono_segmento_lonlat(lista_total[i], datos.L)
                point_in_edge = ap.punto_en_poligono(poligono, datos.longitud, datos.latitud)
                if point_in_edge:
                    datos.posicion_subsegmento = i
                    datos.coordenadas_subsegmento = lista_total[i]
                    break
        else:
            datos.coordenadas_subsegmento = datos.coordenadas_segmento
            datos.longitud_subsegmento = datos.info_edge['length']
            datos.posicion_subsegmento = 0

# Ejecución principal encapsulada en función para reuso

# NUEVA: procesar un archivo específico y devolver lista de segmentos
# Extraído de la lógica original del bucle dentro de procesar()
def procesar_archivo_especifico(nombre_archivo: str):
    global df_gps  # usado por funciones auxiliares
    try:
        contador_json = 1
        df, _ = ap.cargar_csv_con_metadatos(carpeta_csv, nombre_archivo)
        df_gps = ap.eliminar_muestras_gps_duplicadas(df)
        df_gps = ap.ajustar_heading_y_filtrar(df_gps)
        df_gps = ap.filtrar_muestras_por_velocidad(df_gps, 3)
        datos_mapa = DatosProcesamiento()
        lista_recortes = []
        for i in range(len(df_gps)):
            adquirir_latitud_longitud(datos_mapa, i)
            procesamiento_mapa_simple(datos_mapa)
            ubicar_muestra_grafo(datos_mapa)
            segmentar_grafo(datos_mapa)
            hash_segmento = ap.hash_segmento(
                datos_mapa.id_edge[0],
                datos_mapa.id_edge[1],
                (datos_mapa.posicion_subsegmento * 1000) + datos_mapa.id_edge[2]
            )
            if datos_mapa.cambio_segmento:
                nombre = datos_mapa.info_edge['name'] if 'name' in datos_mapa.info_edge else 'Undefined'
                segmento = {
                    'id': hash_segmento,
                    'nombre': nombre,
                    'tipo_via': datos_mapa.info_edge.get('highway', 'unknown'),
                    'longitud_via': datos_mapa.longitud_subsegmento,
                    'punto_inicial': i,
                    'tiempo': ap.timestamp_a_iso8601(int(df_gps['timestamp'].iloc[i])),
                    'coordenadas_segmento': datos_mapa.coordenadas_subsegmento
                }
                lista_recortes.append(segmento)
        # Construcción JSON (idéntico a procesar())
        resultado_json = []
        for i in range(len(lista_recortes)):
            lista_geometria = []
            for j in range(len(lista_recortes[i]['coordenadas_segmento'])):
                puntos = {
                    'orden': j,
                    'longitud': lista_recortes[i]['coordenadas_segmento'][j][0],
                    'latitud': lista_recortes[i]['coordenadas_segmento'][j][1]
                }
                lista_geometria.append(puntos)
            lista_huecos = []
            hueco1 = {
                'latitud': lista_geometria[0]['latitud'],
                'longitud': lista_geometria[0]['longitud'],
                'magnitud': float(np.random.randint(0, 5000) / 1000),
                'velocidad': float(np.random.randint(0, 5000) / 1000),
            }
            hueco2 = {
                'latitud': lista_geometria[-1]['latitud'],
                'longitud': lista_geometria[-1]['longitud'],
                'magnitud': float(np.random.randint(0, 5000) / 1000),
                'velocidad': float(np.random.randint(0, 5000) / 1000),
            }
            lista_huecos.extend([hueco1, hueco2])
            datos_obtenidos = {
                'numero': i,
                'id': lista_recortes[i]['id'],
                'nombre': lista_recortes[i]['nombre'],
                'longitud': lista_recortes[i]['longitud_via'],
                'tipo': lista_recortes[i]['tipo_via'],
                'latitud_origen': lista_geometria[0]['latitud'],
                'latitud_destino': lista_geometria[-1]['latitud'],
                'longitud_origen': lista_geometria[0]['longitud'],
                'longitud_destino': lista_geometria[-1]['longitud'],
                'geometria': lista_geometria,
                'fecha': lista_recortes[i]['tiempo'],
                'IQR': float(np.random.randint(0, 5000) / 1000),
                'iri': float(np.random.randint(0, 20000) / 1000),
                'IRI_modificado': float(np.random.randint(0, 5000) / 1000),
                'az': float(np.random.randint(0, 5000) / 1000),
                'ax': float(np.random.randint(0, 5000) / 1000),
                'wx': float(np.random.randint(0, 5000) / 1000),
                'huecos': lista_huecos
            }
            resultado_json.append(datos_obtenidos)
        if len(resultado_json) > 0:
            print(f'[main_procesamiento] guardando datos archivo: {nombre_archivo}')
            os.makedirs(carpeta_archivos_json, exist_ok=True)
            ruta_archivo = os.path.join(carpeta_archivos_json, 'datos' + str(contador_json) + '.json')
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(resultado_json, archivo, ensure_ascii=False, indent=2)
            os.makedirs(carpeta_almacenamiento_json, exist_ok=True)
            ruta_archivo2 = os.path.join(carpeta_almacenamiento_json, 'datos' + nombre_archivo[:-4] + 'save.json')
            with open(ruta_archivo2, 'w', encoding='utf-8') as archivo:
                json.dump(resultado_json, archivo, ensure_ascii=False, indent=2)
            ab.mover_archivo(carpeta_csv, carpeta_almacenamiento_csv, nombre_archivo)
        return resultado_json
    except Exception as e:
        print('[main_procesamiento][ERROR] procesar_archivo_especifico:', e)
        return []

# Ajustado: procesar todos usando la función nueva
def procesar():
    listado_csv_encontrados = ab.buscar_archivos_por_nombre(carpeta_csv, prefijo_busqueda)
    for dato in listado_csv_encontrados:
        procesar_archivo_especifico(dato)
    return True

if __name__ == '__main__':
    procesar()
