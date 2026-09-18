-- OREGUNTAR SI HACE FALTA PONER CREATE...EXIXST PARA CADA TABLA
-- VER FRANJA HORARIA
--DROP DATABASE IF exists club_Deportivo;
CREATE DATABASE IF NOT EXISTS Club_Deportivo;

USE Club_Deportivo;

CREATE TABLE Deportes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	deporte varchar (50)
);

CREATE TABLE Canchas (
    id_cancha int PRIMARY KEY,
    id_deporte int,
    nombre_cancha varchar(20),
    Disponibilidad boolean, -- si alguien la reservo o no
    precio_hora int,
    Techada boolean DEFAULT false, -- VEMOS
    Activa boolean DEFAULT true, -- si se puede usar o no 
    Horario_inicio Time, -- ver
    Horario_fin Time -- ver

    FOREIGN KEY (id_deporte) REFERENCES Deportes(id)
);


CREATE TABLE Socios (
    id_socio INT AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50),
    mail varchar(50), -- falta exp reg para probar validez
    activo boolean DEFAULT true
);

CREATE TABLE Reservas (
    numero_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT, -- NO VACIO
    nombre_cancha varchar(20), -- MO VACIO
    estado varchar(20),
    fecha_desde DATETIME,
    fecha_hasta DATETIME,
    precio_hora INT,
    precio_total INT,


    FOREIGN KEY (id_socio) REFERENCES Socios(id_socio),
    FOREIGN KEY (id_cancha) REFERENCES Canchas(id_cancha)
);


INSERT INTO Socios (nombre, mail) VALUES
    ('Marani, Baltazar',  'bmarani@fi.uba.ar'),
    ('Daglio, Cristian', 'cdaglio@fi.ub.ar'),
    ('Piccicacco, Leandro', 'lpiccicacco@fi.uba.ar'),
    ('Roberti, Gaston', 'groberti@fi.uba.ar'),
    ('Hernandez, Lucia', 'lhernandez@fi.uba.ar'),
    ('Blazek, Alexis', 'ablazek@fi.uba.ar'),
    ('Perata, Agustin', 'aperata@fi.uba.ar');


INSERT INTO Canchas
(idDeporte, nombre_cancha, disponibilidad, precio_hora, Techada, Activa, Horario_inicio, Horario_fin)
VALUES
    (1, 'Cancha Fútbol 1', true, 8000, false, true, '08:00:00', '23:00:00'),
    (1, 'Cancha Fútbol 2', true, 8000, true, true, '08:00:00', '23:00:00'),
    (2, 'Cancha Tenis 1', true, 5000, false, true, '08:00:00', '23:00:00'),
    (2, 'Cancha Tenis 2', false, 5000, false, true, '08:00:00', '23:00:00'),
    (4, 'Cancha Pádel 1', true, 7000, true, true, '08:00:00', '23:00:00');

