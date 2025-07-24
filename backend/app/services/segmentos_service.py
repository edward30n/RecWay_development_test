from typing import List, Optional
from app.db.database import database
from app.schemas.segmentos import SegmentoCreate, Segmento, GeometriaCreate, IndicesSegmentoCreate, HuecoSegmentoCreate
from app.schemas.responses import GeoJSONFeatureCollection, GeoJSONFeature, GeoJSONGeometry, GeoJSONProperties, SegmentoCompleto

class SegmentoService:
    """Servicio para manejar operaciones de segmentos"""
    
    async def get_all_segmentos(self) -> List[Segmento]:
        """Obtener todos los segmentos"""
        async with database.get_connection() as conn:
            rows = await conn.fetch("SELECT * FROM segmento ORDER BY id_segmento")
            return [Segmento(**dict(row)) for row in rows]
    
    async def get_segmento_by_id(self, id_segmento: int) -> Optional[Segmento]:
        """Obtener un segmento por ID"""
        async with database.get_connection() as conn:
            row = await conn.fetchrow("SELECT * FROM segmento WHERE id_segmento = $1", id_segmento)
            return Segmento(**dict(row)) if row else None
    
    async def create_segmento(self, segmento: SegmentoCreate) -> Segmento:
        """Crear un nuevo segmento"""
        async with database.get_connection() as conn:
            query = """
            INSERT INTO segmento (nombre, tipo, nodo_inicial_x, nodo_final_x, nodo_inicial_y, 
                                nodo_final_y, cantidad_muestras, ultima_fecha_muestra, longitud,
                                oneway, surface, width, error_gps)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            RETURNING *
            """
            row = await conn.fetchrow(
                query, 
                segmento.nombre, segmento.tipo, segmento.nodo_inicial_x, segmento.nodo_final_x,
                segmento.nodo_inicial_y, segmento.nodo_final_y, segmento.cantidad_muestras,
                segmento.ultima_fecha_muestra, segmento.longitud, segmento.oneway,
                segmento.surface, segmento.width, segmento.error_gps
            )
            return Segmento(**dict(row))
    
    async def get_geometrias_by_segmento(self, id_segmento: int):
        """Obtener las geometrías de un segmento"""
        async with database.get_connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM geometria WHERE id_segmento_seleccionado = $1 ORDER BY orden", 
                id_segmento
            )
            return [dict(row) for row in rows]
    
    async def get_indices_by_segmento(self, id_segmento: int):
        """Obtener los índices de un segmento"""
        async with database.get_connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM indicesSegmento WHERE id_segmento_seleccionado = $1", 
                id_segmento
            )
            return dict(row) if row else None
    
    async def get_huecos_by_segmento(self, id_segmento: int):
        """Obtener los huecos de un segmento"""
        async with database.get_connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM huecoSegmento WHERE id_segmento_seleccionado = $1", 
                id_segmento
            )
            return [dict(row) for row in rows]
    
    async def get_segmentos_geojson(self) -> GeoJSONFeatureCollection:
        """Obtener todos los segmentos en formato GeoJSON"""
        async with database.get_connection() as conn:
            # Query principal que une segmentos con sus geometrías e índices
            query = """
            SELECT 
                s.*,
                COALESCE(i.nota_general, 0) as nota_general,
                COALESCE(i.iri_modificado, 0) as iri_modificado,
                COALESCE(i.iri_estandar, 0) as iri_estandar,
                array_agg(ARRAY[g.coordenada_x, g.coordenada_y] ORDER BY g.orden) as coordinates
            FROM segmento s
            LEFT JOIN indicesSegmento i ON s.id_segmento = i.id_segmento_seleccionado
            LEFT JOIN geometria g ON s.id_segmento = g.id_segmento_seleccionado
            GROUP BY s.id_segmento, i.nota_general, i.iri_modificado, i.iri_estandar
            ORDER BY s.id_segmento
            """
            
            rows = await conn.fetch(query)
            features = []
            
            for row in rows:
                # Si no hay geometrías, usar los puntos inicial y final
                if row['coordinates'] and row['coordinates'][0]:
                    coordinates = [list(coord) for coord in row['coordinates']]
                else:
                    coordinates = [
                        [row['nodo_inicial_x'], row['nodo_inicial_y']],
                        [row['nodo_final_x'], row['nodo_final_y']]
                    ]
                
                feature = GeoJSONFeature(
                    geometry=GeoJSONGeometry(
                        type="LineString",
                        coordinates=coordinates
                    ),
                    properties=GeoJSONProperties(
                        id_segmento=row['id_segmento'],
                        nombre=row['nombre'],
                        tipo=row['tipo'],
                        cantidad_muestras=row['cantidad_muestras'],
                        ultima_fecha_muestra=row['ultima_fecha_muestra'],
                        longitud=row['longitud'],
                        nota_general=row['nota_general'],
                        iri_modificado=row['iri_modificado'],
                        iri_estandar=row['iri_estandar']
                    )
                )
                features.append(feature)
            
            return GeoJSONFeatureCollection(features=features)

# Instancia del servicio
segmento_service = SegmentoService()
