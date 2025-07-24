-- Script de inicialización de la base de datos RecWay v2.0
-- Nota: La base de datos debe estar creada previamente

-- ELIMINACIÓN DE TABLAS EN ORDEN CORRECTO PARA EVITAR ERRORES (OPCIONAL)
-- DROP TABLE IF EXISTS registro_sensores;
-- DROP TABLE IF EXISTS indices_muestra;
-- DROP TABLE IF EXISTS huecoMuestra;
-- DROP TABLE IF EXISTS muestra;
-- DROP TABLE IF EXISTS huecoSegmento;
-- DROP TABLE IF EXISTS indicesSegmento;
-- DROP TABLE IF EXISTS geometria;
-- DROP TABLE IF EXISTS segmento;
-- DROP TABLE IF EXISTS fuente_datos_dispositivo;

-- TABLA PRINCIPAL: SEGMENTO
CREATE TABLE IF NOT EXISTS segmento (
    id_segmento bigserial PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    tipo varchar(50),
    nodo_inicial_x double precision NOT NULL,
    nodo_final_x double precision NOT NULL,
    nodo_inicial_y double precision NOT NULL,
    nodo_final_y double precision NOT NULL,
    cantidad_muestras integer NOT NULL,
    ultima_fecha_muestra varchar(30),
    longitud double precision NOT NULL,
    oneway boolean,
    surface integer,
    width double precision,
    error_gps double precision
);

-- GEOMETRÍA DEL SEGMENTO
CREATE TABLE IF NOT EXISTS geometria (
    id_geometria bigserial PRIMARY KEY,
    orden integer NOT NULL,
    coordenada_x double precision NOT NULL,
    coordenada_y double precision NOT NULL,
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- ÍNDICES CALCULADOS DEL SEGMENTO
CREATE TABLE IF NOT EXISTS indicesSegmento (
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

-- HUECOS ASOCIADOS AL SEGMENTO
CREATE TABLE IF NOT EXISTS huecoSegmento (
    id_hueco_segmento bigserial PRIMARY KEY,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    magnitud double precision NOT NULL,
    velocidad double precision NOT NULL,
    ultima_fecha_muestra varchar(30),
    error_gps double precision,
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- MUESTRAS (GRABACIONES DE UN USUARIO EN UN SEGMENTO)
CREATE TABLE IF NOT EXISTS muestra (
    id_muestra bigserial PRIMARY KEY,
    tipo_dispositivo varchar(30),
    identificador_dispositivo varchar(60),
    fecha_muestra varchar(40),
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- ÍNDICES CALCULADOS POR MUESTRA
CREATE TABLE IF NOT EXISTS indices_muestra (
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

-- HUECOS INDIVIDUALIZADOS POR MUESTRA
CREATE TABLE IF NOT EXISTS huecoMuestra (
    id_hueco_muestra bigserial PRIMARY KEY,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    magnitud double precision NOT NULL,
    velocidad double precision NOT NULL,
    id_muestra_seleccionada integer NOT NULL,
    FOREIGN KEY (id_muestra_seleccionada) REFERENCES muestra(id_muestra) ON DELETE CASCADE
);

-- METAINFORMACIÓN DEL DISPOSITIVO QUE ENVÍA LA INFORMACIÓN
CREATE TABLE IF NOT EXISTS fuente_datos_dispositivo (
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
    android_id varchar(100),
    battery_info varchar(100),
    acc_available boolean,
    acc_info varchar(100),
    gyro_available boolean,
    gyro_info varchar(100),
    gps_available boolean,
    gps_info varchar(100),
    export_date timestamp,
    total_records integer,
    sampling_rate real,
    recording_duration varchar(20),
    average_sample_rate real
);

-- REGISTRO DETALLADO DE CADA MUESTRA DE SENSOR
CREATE TABLE IF NOT EXISTS registro_sensores (
    id_registro bigserial PRIMARY KEY,
    timestamp bigint NOT NULL,
    acc_x double precision,
    acc_y double precision,
    acc_z double precision,
    acc_magnitude double precision,
    gyro_x double precision,
    gyro_y double precision,
    gyro_z double precision,
    gyro_magnitude double precision,
    gps_lat double precision,
    gps_lng double precision,
    gps_accuracy double precision,
    gps_speed double precision,
    gps_speed_accuracy double precision,
    gps_altitude double precision,
    gps_altitude_accuracy double precision,
    gps_heading double precision,
    gps_heading_accuracy double precision,
    gps_timestamp bigint,
    gps_provider varchar(50),
    device_orientation double precision,
    sample_rate double precision,
    gps_changed boolean DEFAULT false,
    id_fuente integer NOT NULL,
    FOREIGN KEY (id_fuente) REFERENCES fuente_datos_dispositivo(id_fuente) ON DELETE CASCADE
);

-- CREAR ÍNDICES PARA MEJORAR EL RENDIMIENTO
CREATE INDEX IF NOT EXISTS idx_geometria_segmento ON geometria(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_geometria_orden ON geometria(orden);
CREATE INDEX IF NOT EXISTS idx_indices_segmento ON indicesSegmento(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_hueco_segmento ON huecoSegmento(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_muestra_segmento ON muestra(id_segmento_seleccionado);
CREATE INDEX IF NOT EXISTS idx_indices_muestra ON indices_muestra(id_muestra);
CREATE INDEX IF NOT EXISTS idx_hueco_muestra ON huecoMuestra(id_muestra_seleccionada);
CREATE INDEX IF NOT EXISTS idx_registro_fuente ON registro_sensores(id_fuente);
CREATE INDEX IF NOT EXISTS idx_registro_timestamp ON registro_sensores(timestamp);
CREATE INDEX IF NOT EXISTS idx_registro_gps ON registro_sensores(gps_lat, gps_lng);

-- COMENTARIOS PARA DOCUMENTACIÓN
COMMENT ON TABLE segmento IS 'Tabla principal de segmentos de carretera con información geográfica y características';
COMMENT ON TABLE geometria IS 'Puntos que definen la geometría exacta de cada segmento';
COMMENT ON TABLE indicesSegmento IS 'Índices de calidad calculados para cada segmento (IRI, notas, etc.)';
COMMENT ON TABLE huecoSegmento IS 'Huecos detectados y agregados por segmento';
COMMENT ON TABLE muestra IS 'Muestras individuales de datos recolectadas por dispositivos en segmentos';
COMMENT ON TABLE indices_muestra IS 'Índices de calidad calculados para cada muestra individual';
COMMENT ON TABLE huecoMuestra IS 'Huecos individuales detectados en cada muestra';
COMMENT ON TABLE fuente_datos_dispositivo IS 'Metainformación de dispositivos que recolectan datos';
COMMENT ON TABLE registro_sensores IS 'Registros detallados de sensores (acelerómetro, giroscopio, GPS) por dispositivo';
