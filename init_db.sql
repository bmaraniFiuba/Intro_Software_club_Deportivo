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


DELETE FROM alumnos; -- sin WHERE, se comporta como "TRUNCATE TABLE alumnos;"

DELETE FROM alumnos WHERE padron > 2;

DROP TABLE alumnos;

DROP DATABASE IDS_test;

-- agrego columna
ALTER TABLE alumnos ADD COLUMN fecha_egreso DATETIME;

-- borro columna
ALTER TABLE alumnos drop COLUMN fecha_egreso;

-- agrego varias
ALTER TABLE alumnos ADD (
	fecha_egreso DATETIME,
	nota_maxima decimal(2,1)
);

ALTER TABLE alumnos drop COLUMN fecha_egreso;
ALTER TABLE alumnos drop COLUMN nota_maxima;

-- agrego varias con valores por defecto
ALTER TABLE alumnos ADD (
	fecha_egreso DATETIME DEFAULT "9999-12-31",
	nota_maxima decimal(2,1)
);

SELECT * FROM alumnos WHERE padron >= 3;

SELECT padron, nombre, apellido FROM alumnos WHERE padron IN (3, 5);

SELECT padron, nombre, apellido FROM alumnos WHERE padron BETWEEN 3 AND 5;

SELECT padron, nombre, apellido FROM alumnos WHERE NOMBRE LIKE '%pe%';
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------



