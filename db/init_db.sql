DROP DATABASE IF EXISTS Club_Deportivo;
CREATE DATABASE Club_Deportivo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE Club_Deportivo;

SET NAMES utf8mb4;

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
    techada BOOLEAN NOT NULL DEFAULT FA    Invoke-RestMethod "http://127.0.0.1:8080/club_deportivo_encuentro/canchas/1"    Invoke-RestMethod "http://127.0.0.1:8080/club_deportivo_encuentro/canchas/1"LSE,
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