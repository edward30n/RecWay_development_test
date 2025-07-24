-- Datos de ejemplo para probar la aplicación RecWay

-- Insertar segmentos de ejemplo
INSERT INTO segmento (id_segmento, nombre, tipo, latitud_origen, latitud_destino, longitud_origen, longitud_destino, cantidad_muestras, ultima_fecha_muestra, longitud) VALUES
(1, 'Autopista Norte Tramo 1', 'Autopista', 4.7110, 4.7150, -74.0721, -74.0701, 5, '2024-01-15', 2.5),
(2, 'Carrera 7 Centro', 'Vía Principal', 4.5981, 4.6021, -74.0758, -74.0738, 3, '2024-01-10', 1.8),
(3, 'Calle 26 Aeropuerto', 'Vía Arterial', 4.6097, 4.6137, -74.1066, -74.1046, 7, '2024-01-20', 3.2);

-- Insertar geometrías para los segmentos
INSERT INTO geometria (orden, longitud, latitud, id_segmento_seleccionado) VALUES
-- Segmento 1
(1, -74.0721, 4.7110, 1),
(2, -74.0711, 4.7120, 1),
(3, -74.0701, 4.7150, 1),
-- Segmento 2
(1, -74.0758, 4.5981, 2),
(2, -74.0748, 4.6001, 2),
(3, -74.0738, 4.6021, 2),
-- Segmento 3
(1, -74.1066, 4.6097, 3),
(2, -74.1056, 4.6117, 3),
(3, -74.1046, 4.6137, 3);

-- Insertar índices para los segmentos
INSERT INTO indicesSegmento (nota_general, iri_modificado, iri_estandar, indice_primero, indice_segundo, iri_tercero, id_segmento_seleccionado) VALUES
(8.5, 2.3, 2.1, 8.2, 8.8, 2.5, 1),
(7.2, 3.1, 2.8, 7.0, 7.4, 3.2, 2),
(6.8, 3.8, 3.5, 6.5, 7.1, 4.0, 3);

-- Insertar algunos huecos en segmentos
INSERT INTO huecoSegmento (latitud, longitud, magnitud, velocidad, ultima_fecha_muestra, id_segmento_seleccionado) VALUES
(4.7115, -74.0716, 2.5, 45.0, '2024-01-15', 1),
(4.7125, -74.0706, 1.8, 42.0, '2024-01-15', 1),
(4.6001, -74.0748, 3.2, 35.0, '2024-01-10', 2),
(4.6127, -74.1051, 4.1, 55.0, '2024-01-20', 3);

-- Insertar muestras
INSERT INTO muestra (tipo_dispositivo, identificador_dispositivo, fecha_muestra, id_segmento_seleccionado) VALUES
('Smartphone', 'DEVICE_001', '2024-01-15 10:30:00', 1),
('Smartphone', 'DEVICE_002', '2024-01-15 14:20:00', 1),
('Tablet', 'DEVICE_003', '2024-01-10 09:15:00', 2),
('Smartphone', 'DEVICE_004', '2024-01-20 16:45:00', 3),
('Smartphone', 'DEVICE_005', '2024-01-20 11:30:00', 3);

-- Insertar índices para las muestras
INSERT INTO indicesMuestra (nota_general, iri_modificado, iri_estandar, indice_primero, indice_segundo, iri_tercero, id_muestra_seleccionada) VALUES
(8.3, 2.4, 2.2, 8.1, 8.5, 2.6, 1),
(8.7, 2.2, 2.0, 8.4, 9.0, 2.4, 2),
(7.1, 3.2, 2.9, 6.9, 7.3, 3.3, 3),
(6.9, 3.7, 3.4, 6.6, 7.2, 3.9, 4),
(6.7, 3.9, 3.6, 6.4, 7.0, 4.1, 5);

-- Insertar huecos en muestras
INSERT INTO huecoMuestra (latitud, longitud, magnitud, velocidad, id_muestra_seleccionada) VALUES
(4.7115, -74.0716, 2.4, 44.0, 1),
(4.7125, -74.0706, 1.9, 43.0, 2),
(4.6001, -74.0748, 3.1, 36.0, 3),
(4.6127, -74.1051, 4.0, 54.0, 4),
(4.6130, -74.1048, 3.5, 56.0, 5);
