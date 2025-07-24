-- Script de inicialización de la base de datos RecWay v2.0
-- Este archivo se ejecuta automáticamente cuando Docker inicia PostgreSQL por primera vez

-- ELIMINACIÓN DE TABLAS EN ORDEN CORRECTO PARA EVITAR ERRORES
DROP TABLE IF EXISTS registro_sensores;
DROP TABLE IF EXISTS indices_muestra;
DROP TABLE IF EXISTS huecoMuestra;
DROP TABLE IF EXISTS muestra;
DROP TABLE IF EXISTS huecoSegmento;
DROP TABLE IF EXISTS indicesSegmento;
DROP TABLE IF EXISTS geometria;
DROP TABLE IF EXISTS segmento;
DROP TABLE IF EXISTS fuente_datos_dispositivo;

-- TABLA PRINCIPAL: SEGMENTO
CREATE TABLE segmento (
    id_segmento bigserial PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    descripcion text,
    longitud double precision NOT NULL,
    latitud double precision NOT NULL,
    ubicacion varchar(100),
    tipo varchar(50),
    nodo_inicial_x double precision,
    nodo_final_x double precision,
    nodo_inicial_y double precision,
    nodo_final_y double precision,
    cantidad_muestras integer DEFAULT 0,
    ultima_fecha_muestra timestamp,
    oneway boolean DEFAULT false,
    surface integer,
    width double precision,
    error_gps double precision,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- GEOMETRÍA DEL SEGMENTO
CREATE TABLE geometria (
    id_geometria bigserial PRIMARY KEY,
    orden integer NOT NULL,
    coordenada_x double precision NOT NULL,
    coordenada_y double precision NOT NULL,
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- ÍNDICES CALCULADOS DEL SEGMENTO
CREATE TABLE indicesSegmento (
    id_indice_segmento bigserial PRIMARY KEY,
    nota_general double precision NOT NULL,
    iri_modificado double precision NOT NULL,
    iri_estandar double precision NOT NULL,
    indice_primero double precision NOT NULL,
    indice_segundo double precision NOT NULL,
    iri_tercero double precision,
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- MUESTRAS (GRABACIONES DE UN USUARIO EN UN SEGMENTO)
CREATE TABLE muestra (
    id_muestra bigserial PRIMARY KEY,
    tipo_dispositivo varchar(30),
    identificador_dispositivo varchar(60),
    fecha_muestra timestamp,
    id_segmento_seleccionado integer NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- ÍNDICES CALCULADOS POR MUESTRA
CREATE TABLE indices_muestra (
    id_indice_muestra bigserial PRIMARY KEY,
    nota_general double precision NOT NULL,
    iri_modificado double precision NOT NULL,
    iri_estandar double precision NOT NULL,
    indice_primero double precision NOT NULL,
    indice_segundo double precision NOT NULL,
    iri_tercero double precision,
    id_muestra integer NOT NULL,
    FOREIGN KEY (id_muestra) REFERENCES muestra(id_muestra) ON DELETE CASCADE
);

-- METAINFORMACIÓN DEL DISPOSITIVO QUE ENVÍA LA INFORMACIÓN
CREATE TABLE fuente_datos_dispositivo (
    id_fuente bigserial PRIMARY KEY,
    device_id varchar(100),
    session_id varchar(100),
    platform varchar(50),
    device_model varchar(100),
    manufacturer varchar(100),
    brand varchar(100),
    os_version varchar(50),
    app_version varchar(100),
    company varchar(100),
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- CREAR ÍNDICES PARA MEJORAR EL RENDIMIENTO
CREATE INDEX IF NOT EXISTS idx_geometria_segmento ON geometria(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_geometria_orden ON geometria(orden);
CREATE INDEX IF NOT EXISTS idx_indices_segmento ON indicesSegmento(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_muestra_segmento ON muestra(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_indices_muestra ON indices_muestra(id_muestra);

-- INSERTAR DATOS DE PRUEBA
INSERT INTO segmento (nombre, descripcion, longitud, latitud, ubicacion) VALUES
('Carretera Central Km 50', 'Segmento de prueba principal', -76.935242, -12.046374, 'Lima, Perú'),
('Av. Javier Prado Este', 'Avenida principal de San Isidro', -77.027442, -12.094373, 'San Isidro, Lima'),
('Panamericana Sur Km 25', 'Carretera hacia el sur', -77.042944, -12.204373, 'Villa El Salvador, Lima');

-- COMENTARIOS PARA DOCUMENTACIÓN
COMMENT ON TABLE segmento IS 'Tabla principal de segmentos de carretera con información geográfica y características';
COMMENT ON TABLE geometria IS 'Puntos que definen la geometría exacta de cada segmento';
COMMENT ON TABLE indicesSegmento IS 'Índices de calidad calculados para cada segmento (IRI, notas, etc.)';
COMMENT ON TABLE muestra IS 'Muestras individuales de datos recolectadas por dispositivos en segmentos';
COMMENT ON TABLE indices_muestra IS 'Índices de calidad calculados para cada muestra individual';
COMMENT ON TABLE fuente_datos_dispositivo IS 'Metainformación de dispositivos que recolectan datos';

-- Confirmar que el script se ejecutó correctamente
\echo 'Database RecWay initialized successfully with tables and sample data!';
