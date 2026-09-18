DROP DATABASE IF EXISTS Club_Deportivo;
CREATE DATABASE Club_Deportivo;

USE Club_Deportivo;


-- =========================
-- TABLA DEPORTES
-- =========================

CREATE TABLE Deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    deporte VARCHAR(50)
);


-- =========================
-- TABLA CANCHAS
-- =========================

CREATE TABLE Canchas (
    id_cancha INT AUTO_INCREMENT PRIMARY KEY,
    id_deporte INT,
    nombre_cancha VARCHAR(20),
    disponibilidad BOOLEAN,
    precio_hora INT,
    Techada BOOLEAN DEFAULT false,
    Activa BOOLEAN DEFAULT true,
    Horario_inicio TIME,
    Horario_fin TIME,

    FOREIGN KEY (id_deporte) REFERENCES Deportes(id)
);


-- =========================
-- TABLA SOCIOS
-- =========================

CREATE TABLE Socios (
    id_socio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    mail VARCHAR(50),
    activo BOOLEAN DEFAULT true
);


-- =========================
-- TABLA RESERVAS
-- =========================

CREATE TABLE Reservas (
    numero_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT,
    id_cancha INT,
    estado VARCHAR(20),
    fecha_desde DATETIME,
    fecha_hasta DATETIME,
    precio_hora INT,
    precio_total INT,

    FOREIGN KEY (id_socio) REFERENCES Socios(id_socio),
    FOREIGN KEY (id_cancha) REFERENCES Canchas(id_cancha)
);


-- =========================
-- INSERTAR DEPORTES
-- =========================

INSERT INTO Deportes (deporte) VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Básquet'),
    ('Pádel');


-- =========================
-- INSERTAR SOCIOS
-- =========================

INSERT INTO Socios (nombre, mail) VALUES
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

INSERT INTO Canchas
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