-- OREGUNTAR SI HACE FALTA PONER CREATE...EXIXST PARA CADA TABLA
-- VER FRANJA HORARIA
--DROP DATABASE IF exists club_Deportivo;
CREATE DATABASE IF NOT EXISTS club_Deportivo;

USE club_Deportivo;

CREATE TABLE Deportes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	deporte varchar (50)
);

CREATE TABLE Canchas (
    id_cancha int PRIMARY KEY,
    idDeporte int,
    nombre_cancha varchar(20),
    Disponibilidad boolean, -- si alguien la reservo o no
    precio_hora int,
    Techada boolean DEFAULT false, -- VEMOS
    Activa boolean DEFAULT true, -- si se puede usar o no 
    Horario_inicio Time, -- ver
    Horario_fin Time -- ver
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


    FOREIGN KEY (id_socio) REFERENCES Socios(id_socio),
    FOREIGN KEY (id_cancha) REFERENCES Canchas(id_cancha)
);


