DROP DATABASE IF EXISTS Club_Deportivo;
CREATE DATABASE Club_Deportivo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE Club_Deportivo;

SET NAMES utf8mb4; -- para que los acentos se guarden correctamente en la base de datos 


-- =========================
-- TABLA DEPORTES
-- =========================
CREATE TABLE deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- =========================
-- TABLA CANCHAS
-- =========================
CREATE TABLE canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_deporte INT NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

-- =========================
-- TABLA SOCIOS
-- =========================
CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT true
);

-- =========================
-- TABLA RESERVAS
-- =========================
CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    estado VARCHAR(30),
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,

    FOREIGN KEY (id_socio) REFERENCES socios(id),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id)
);

-- =========================
-- INSERTAR DEPORTES
-- =========================
INSERT INTO deportes (nombre) VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');

-- =========================
-- INSERTAR SOCIOS
-- =========================
INSERT INTO socios (nombre, email) VALUES
    ('Marani, Baltazar', 'bmarani@fi.uba.ar'),
    ('Daglio, Cristian', 'cdaglio@fi.uba.ar'),
    ('Piccicacco, Leandro', 'lpiccicacco@fi.uba.ar'),
    ('Roberti, Gaston', 'groberti@fi.uba.ar'),
    ('Hernandez, Lucia', 'lhernandez@fi.uba.ar'),
    ('Blazek, Alexis', 'ablazek@fi.uba.ar'),
    ('Perata, Agustin', 'aperata@fi.uba.ar');

-- =========================
-- INSERTAR CANCHAS
-- =========================
-- ID Deportes: 1=Fútbol, 2=Tenis, 3=Pádel
INSERT INTO canchas (id_deporte, nombre, precio_hora, techada, activa) VALUES
    (1, 'Cancha Fútbol 1', 800000, false, true),
    (1, 'Cancha Fútbol 2', 800000, true, true),
    (2, 'Cancha Tenis 1', 500000, false, true),
    (2, 'Cancha Tenis 2', 500000, false, false),
    (3, 'Cancha Pádel 1', 700000, true, true);

-- =========================
-- INSERTAR RESERVAS
-- =========================
-- Socios: 1=Marani 2=Daglio 3=Piccicacco 4=Roberti 5=Hernandez 6=Blazek 7=Perata
-- Canchas: 1=Fútbol1(800000) 2=Fútbol2(800000) 3=Tenis1(500000) 4=Tenis2(500000,INACTIVA) 5=Pádel1(700000)

INSERT INTO reservas (id_socio, id_cancha, estado, fecha_hora_inicio, fecha_hora_fin, precio_hora, precio_total) VALUES
    -- 1) Pasada, finalizada normalmente
    (1, 1, 'finalizada', '2026-08-05 10:00:00', '2026-08-05 12:00:00', 800000, 1600000),

    -- 2) Pasada, fue cancelada antes de que empezara
    (2, 2, 'cancelada',  '2026-08-12 18:00:00', '2026-08-12 19:00:00', 800000, 800000),

    -- 3) Cancha 4 (Tenis2) está INACTIVA hoy, pero tiene una reserva vieja
    --    -> caso borde: filtrar id_cancha=4 debe traer resultados igual (activa no borra historial)
    (3, 4, 'finalizada', '2026-09-01 09:00:00', '2026-09-01 10:00:00', 500000, 500000),

    -- 4) Pasada reciente, finalizada
    (4, 1, 'finalizada', '2026-09-20 20:00:00', '2026-09-20 22:00:00', 800000, 1600000),

    -- 5) y 6) MISMO DÍA (2026-10-15), canchas distintas
    --    -> caso borde: fecha_desde=fecha_hasta=2026-10-15 debe traer ambas
    (5, 3, 'confirmada', '2026-10-15 18:00:00', '2026-10-15 20:00:00', 500000, 1000000),
    (6, 5, 'confirmada', '2026-10-15 09:00:00', '2026-10-15 10:00:00', 700000, 700000),

    -- 7) y 8) CONSECUTIVAS en la misma cancha (20-21 y 21-22)
    --    -> caso válido de negocio, no un conflicto (a diferencia de superponerse)
    (7, 1, 'confirmada', '2026-10-20 20:00:00', '2026-10-20 21:00:00', 800000, 800000),
    (1, 1, 'confirmada', '2026-10-20 21:00:00', '2026-10-20 22:00:00', 800000, 800000),

    -- 9) Borde de apertura del club (08:00) y 10) borde de cierre (hasta 23:00)
    (2, 2, 'confirmada', '2026-10-25 08:00:00', '2026-10-25 09:00:00', 800000, 800000),
    (3, 2, 'confirmada', '2026-10-25 22:00:00', '2026-10-25 23:00:00', 800000, 800000),

    -- 11) Duración máxima permitida (3 horas)
    (4, 3, 'confirmada', '2026-11-01 08:00:00', '2026-11-01 11:00:00', 500000, 1500000),

    -- 12) Pasada y cancelada (probar que se pueden consultar reservas pasadas sin importar el estado)
    (5, 5, 'cancelada',  '2026-09-10 14:00:00', '2026-09-10 15:00:00', 700000, 700000),

    -- 13) Pasada pero SIGUE "confirmada" (nadie la finalizó a mano)
    --    -> caso borde clave: el enunciado dice que los cambios de estado son explícitos,
    --       así que una reserva vencida puede seguir figurando como confirmada
    (6, 3, 'confirmada', '2026-09-05 10:00:00', '2026-09-05 11:00:00', 500000, 500000);
