-- OREGUNTAR SI HACE FALTA PONER CREATE...EXIXST PARA CADA TABLA
-- VER FRANJA HORARIA

CREATE DATABASE club_Deportivo IF NOT EXISTS club_Deportivo;

USE club_Deportivo;

CREATE TABLE Deportes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	deporte varchar (50)
);

CREATE TABLE Canchas (
    idDeporte int(2),
    nombre varchar(20) PRIMARY KEY,
    Disponibilidad boolean, --si alguien la reservo o no
    precio_hora int (10),
    Techada boolean DEFAULT false, --VEMOS
    Activa boolean DEFAULT true -- si se puede usar o no 
    Horario_inicio Time(8), --ver
    Horario_fin Time (23) --ver
);


CREATE TABLE Socio (
    id_socio INT AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50),
    mail varchar(50), -- falta exp reg para probar validez
    activo boolean DEFAULT true,
);

CREATE TABLE Reservas (
    numero_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_socio, -- NO VACIO
    nombre_cancha, -- MO VACIO
    estado varchar(20),
    fecha_desde DATETIME,
    fecha_hasta DATETIME,


    FOREIGN KEY (id_socio) REFERENCES socios(id_socio),
    FOREIGN KEY (id_cancha) REFERENCES canchas(nombre_cancha)
);


