-----------------------------------------------------------------------
-- RECWAY DATABASE SCHEMA - VERSIÓN COMPLETA CON AUTENTICACIÓN
-- Integra sistema de autenticación con la estructura de datos de RecWay
-----------------------------------------------------------------------

-- ELIMINACIÓN DE TABLAS EN ORDEN CORRECTO
DROP TABLE IF EXISTS registro_sensores;
DROP TABLE IF EXISTS indices_muestra;
DROP TABLE IF EXISTS huecoMuestra;
DROP TABLE IF EXISTS muestra;
DROP TABLE IF EXISTS huecoSegmento;
DROP TABLE IF EXISTS indicesSegmento;
DROP TABLE IF EXISTS geometria;
DROP TABLE IF EXISTS segmento;
DROP TABLE IF EXISTS fuente_datos_dispositivo;

-- Tablas de autenticación
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS auth_tokens;
DROP TABLE IF EXISTS current_subscriptions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS subscription_plans;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS countries;

-----------------------------------------------------------------------
-- 1) PAÍSES (SIMPLIFICADO PARA RECWAY)
-----------------------------------------------------------------------
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-----------------------------------------------------------------------
-- 2) PLANES DE SUSCRIPCIÓN PARA RECWAY
-----------------------------------------------------------------------
CREATE TABLE subscription_plans (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,   -- Basic, Professional, Enterprise
    description     TEXT,
    price_usd       NUMERIC(10, 2),
    max_users       INTEGER,                        -- NULL para ilimitado
    max_segments    INTEGER,                        -- Límite de segmentos analizables
    max_samples     INTEGER,                        -- Límite de muestras por mes
    storage_gb      INTEGER,                        -- Almacenamiento para datos de sensores
    support_type    VARCHAR(50),                    -- email, priority, 24/7
    is_popular      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-----------------------------------------------------------------------
-- 3) EMPRESAS
-----------------------------------------------------------------------
CREATE TABLE companies (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL UNIQUE,
    invite_code     VARCHAR(50) UNIQUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active       BOOLEAN DEFAULT TRUE
);

-----------------------------------------------------------------------
-- 4) USUARIOS CON AUTENTICACIÓN
-----------------------------------------------------------------------
CREATE TABLE users (
    id                         BIGSERIAL PRIMARY KEY,
    company_id                 BIGINT REFERENCES companies(id),
    email                      VARCHAR(255) NOT NULL UNIQUE,
    password_hash              TEXT NOT NULL,
    full_name                  VARCHAR(255),
    phone                      VARCHAR(50),
    registered_at              TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity              TIMESTAMP WITH TIME ZONE,
    is_active                  BOOLEAN DEFAULT TRUE,
    is_email_verified          BOOLEAN DEFAULT TRUE,
    email_verification_token   TEXT,
    reset_token                VARCHAR(255),
    reset_token_expires        TIMESTAMP WITH TIME ZONE,
    country_code               CHAR(2) NOT NULL DEFAULT 'CO'
                               REFERENCES countries(code)
                               CHECK (country_code ~ '^[A-Z]{2}$'),
    phone_prefix               VARCHAR(10)
);

-----------------------------------------------------------------------
-- 5) ROLES DEL SISTEMA
-----------------------------------------------------------------------
CREATE TABLE roles (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE user_roles (
    user_id     BIGINT NOT NULL REFERENCES users(id),
    role_id     BIGINT NOT NULL REFERENCES roles(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

-----------------------------------------------------------------------
-- 6) TOKENS DE AUTENTICACIÓN
-----------------------------------------------------------------------
CREATE TABLE auth_tokens (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id),
    token       TEXT NOT NULL,
    expires_at  TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    revoked     BOOLEAN DEFAULT FALSE
);

-----------------------------------------------------------------------
-- 7) SUSCRIPCIONES ACTUALES
-----------------------------------------------------------------------
CREATE TABLE current_subscriptions (
    id                    BIGSERIAL PRIMARY KEY,
    user_id               BIGINT REFERENCES users(id),
    company_id            BIGINT REFERENCES companies(id),
    subscription_plan_id  BIGINT NOT NULL REFERENCES subscription_plans(id),
    start_date            TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_date              TIMESTAMP WITH TIME ZONE,
    is_active             BOOLEAN DEFAULT TRUE,
    source                VARCHAR(50) DEFAULT 'app',
    CHECK (
       (user_id IS NOT NULL AND company_id IS NULL) OR
       (company_id IS NOT NULL AND user_id IS NULL)
    )
);

-----------------------------------------------------------------------
-- 8) ESTRUCTURA DE DATOS DE RECWAY (ORIGINAL)
-----------------------------------------------------------------------

-- TABLA PRINCIPAL: SEGMENTO
CREATE TABLE segmento (
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
    error_gps double precision,
    -- NUEVA COLUMNA: Asociar segmentos a usuarios/empresas
    created_by_user_id BIGINT REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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

-- HUECOS ASOCIADOS AL SEGMENTO
CREATE TABLE huecoSegmento (
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
CREATE TABLE muestra (
    id_muestra bigserial PRIMARY KEY,
    tipo_dispositivo varchar(30),
    identificador_dispositivo varchar(60),
    fecha_muestra varchar(40),
    id_segmento_seleccionado integer NOT NULL,
    -- NUEVA COLUMNA: Asociar muestras a usuarios
    created_by_user_id BIGINT REFERENCES users(id),
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

-- HUECOS INDIVIDUALIZADOS POR MUESTRA
CREATE TABLE huecoMuestra (
    id_hueco_muestra bigserial PRIMARY KEY,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    magnitud double precision NOT NULL,
    velocidad double precision NOT NULL,
    id_muestra_seleccionada integer NOT NULL,
    FOREIGN KEY (id_muestra_seleccionada) REFERENCES muestra(id_muestra) ON DELETE CASCADE
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
    average_sample_rate real,
    -- NUEVA COLUMNA: Asociar dispositivos a usuarios
    created_by_user_id BIGINT REFERENCES users(id)
);

-- REGISTRO DETALLADO DE CADA MUESTRA DE SENSOR
CREATE TABLE registro_sensores (
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

-----------------------------------------------------------------------
-- 9) ÍNDICES PARA OPTIMIZACIÓN
-----------------------------------------------------------------------
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_auth_tokens_user ON auth_tokens(user_id);
CREATE INDEX idx_auth_tokens_token ON auth_tokens(token);
CREATE INDEX idx_current_subscriptions_user ON current_subscriptions(user_id);
CREATE INDEX idx_current_subscriptions_company ON current_subscriptions(company_id);
CREATE INDEX idx_segmento_user ON segmento(created_by_user_id);
CREATE INDEX idx_muestra_user ON muestra(created_by_user_id);
CREATE INDEX idx_fuente_user ON fuente_datos_dispositivo(created_by_user_id);

-- Índices únicos para garantizar una sola suscripción activa
CREATE UNIQUE INDEX uniq_active_subscription_user
        ON current_subscriptions(user_id)
        WHERE is_active;

CREATE UNIQUE INDEX uniq_active_subscription_company
        ON current_subscriptions(company_id)
        WHERE is_active;

-----------------------------------------------------------------------
-- 10) DATOS INICIALES
-----------------------------------------------------------------------

-- Países principales (simplificado)
INSERT INTO countries (code, name) VALUES
('CO', 'Colombia'),
('US', 'United States'),
('MX', 'Mexico'),
('AR', 'Argentina'),
('BR', 'Brazil'),
('CL', 'Chile'),
('PE', 'Peru'),
('EC', 'Ecuador'),
('ES', 'Spain'),
('UK', 'United Kingdom');

-- Planes de suscripción para RecWay
INSERT INTO subscription_plans
(name, description, price_usd, max_users, max_segments, max_samples, storage_gb, support_type, is_popular)
VALUES
('Basic', 'Para análisis básico de vías urbanas', 29.00, 1, 50, 1000, 5, 'email', FALSE),
('Professional', 'Para equipos de ingeniería vial', 99.00, 5, 500, 10000, 50, 'priority', TRUE),
('Enterprise', 'Para organizaciones gubernamentales', 299.00, NULL, NULL, NULL, 500, '24/7', FALSE);

-- Roles del sistema RecWay
INSERT INTO roles (name, description) VALUES
('admin', 'Administrador con acceso completo al sistema'),
('analyst', 'Analista de datos viales con permisos de lectura/escritura'),
('viewer', 'Visualizador con permisos solo de lectura'),
('engineer', 'Ingeniero vial con permisos para crear y analizar segmentos');

-- Usuario administrador por defecto
-- Contraseña: admin123 (hash bcrypt)
INSERT INTO users (email, password_hash, full_name, country_code, is_active)
VALUES ('admin@recway.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Administrador RecWay', 'CO', TRUE);

-- Asignar rol admin al usuario 1
INSERT INTO user_roles (user_id, role_id)
SELECT 1, r.id FROM roles r WHERE r.name = 'admin';

-- Suscripción Enterprise para el admin
INSERT INTO current_subscriptions (user_id, subscription_plan_id, is_active)
SELECT 1, sp.id, TRUE FROM subscription_plans sp WHERE sp.name = 'Enterprise';

-----------------------------------------------------------------------
-- 11) COMENTARIOS FINALES
-----------------------------------------------------------------------
-- La base de datos está lista para:
-- 1. Autenticación por tokens
-- 2. Sistema de roles y permisos
-- 3. Gestión de empresas y suscripciones
-- 4. Análisis de datos viales (RecWay original)
-- 5. Asociación de datos a usuarios específicos
    iri_tercero double precision,
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- HUECOS ASOCIADOS AL SEGMENTO
CREATE TABLE huecoSegmento (
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
CREATE TABLE muestra (
    id_muestra bigserial PRIMARY KEY,
    tipo_dispositivo varchar(30),
    identificador_dispositivo varchar(60),
    fecha_muestra varchar(40),
    id_segmento_seleccionado integer NOT NULL,
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

-- HUECOS INDIVIDUALIZADOS POR MUESTRA
CREATE TABLE huecoMuestra (
    id_hueco_muestra bigserial PRIMARY KEY,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    magnitud double precision NOT NULL,
    velocidad double precision NOT NULL,
    id_muestra_seleccionada integer NOT NULL,
    FOREIGN KEY (id_muestra_seleccionada) REFERENCES muestra(id_muestra) ON DELETE CASCADE
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
CREATE TABLE registro_sensores (
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
CREATE INDEX idx_geometria_segmento ON geometria(id_segmento_seleccionado);
CREATE INDEX idx_geometria_orden ON geometria(orden);
CREATE INDEX idx_indices_segmento ON indicesSegmento(id_segmento_seleccionado);
CREATE INDEX idx_hueco_segmento ON huecoSegmento(id_segmento_seleccionado);
CREATE INDEX idx_muestra_segmento ON muestra(id_segmento_seleccionado);
CREATE INDEX idx_indices_muestra ON indices_muestra(id_muestra);
CREATE INDEX idx_hueco_muestra ON huecoMuestra(id_muestra_seleccionada);
CREATE INDEX idx_registro_fuente ON registro_sensores(id_fuente);
CREATE INDEX idx_registro_timestamp ON registro_sensores(timestamp);
CREATE INDEX idx_registro_gps ON registro_sensores(gps_lat, gps_lng);

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

-- Mensaje de confirmación
SELECT 'Database RecWay initialized successfully with all 9 tables!' as status;
