DROP DATABASE IF EXISTS Club_Deportivo;
CREATE DATABASE Club_Deportivo;

USE Club_Deportivo;


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
    id_socio INT,
    id_cancha INT,
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

INSERT INTO deportes (deporte) VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');


-- =========================
-- INSERTAR SOCIOS
-- =========================

INSERT INTO socios (nombre, mail) VALUES
    ('Marani, Baltazar', 'bmarani@fi.uba.ar'),
    ('Daglio, Cristian', 'cdaglio@fi.ub.ar'),
    ('Piccicacco, Leandro', 'lpiccicacco@fi.uba.ar'),
    ('Roberti, Gaston', 'groberti@fi.uba.ar'),
    ('Hernandez, Lucia', 'lhernandez@fi.uba.ar'),
    ('Blazek, Alexis', 'ablazek@fi.uba.ar'),
    ('Perata, Agustin', 'aperata@fi.uba.ar');


-- =========================
-- INSERTAR CANCHAS
-- =========================

INSERT INTO canchas
(id_deporte, nombre_cancha, disponibilidad, precio_hora, Techada, Activa, Horario_inicio, Horario_fin)
VALUES
    (1, 'Cancha Fútbol 1', true, 8000, false, true, '08:00:00', '23:00:00'),
    (1, 'Cancha Fútbol 2', true, 8000, true, true, '08:00:00', '23:00:00'),
    (2, 'Cancha Tenis 1', true, 5000, false, true, '08:00:00', '23:00:00'),
    (2, 'Cancha Tenis 2', false, 5000, false, true, '08:00:00', '23:00:00'),
    (4, 'Cancha Pádel 1', true, 7000, true, true, '08:00:00', '23:00:00');

-- =========================
-- Vercion ULTRA MEGA CHAT (BORRAR DESPUES)
-- =========================

--hola
