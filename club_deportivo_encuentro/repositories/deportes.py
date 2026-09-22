from club_deportivo_encuentro.db import ejecutar_consulta


def obtener_deportes():
	return ejecutar_consulta('SELECT id, nombre FROM deportes ORDER BY id ASC')
