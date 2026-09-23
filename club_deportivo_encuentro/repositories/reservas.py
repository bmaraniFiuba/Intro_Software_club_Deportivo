from club_deportivo_encuentro.db import (ejecutar_consulta, ejecutar_escritura)
from ..constants import FORMATO_FECHA_HORA


#funciones para metodo GET
def obtener_reservas (filtros: dict, offset:int, limit:int) -> list[dict]:
    cond = [] #lo uso para generar la consulta a la base de datos
    query_params = {}
    
# :algo es un parámetro que después se completa con el valor
# correspondiente dentro de query_params.
    
    if filtros.get('id_socio') is not None:
        cond.append("id_socio = :id_socio")
        query_params["id_socio"] = filtros["id_socio"]
    

    if filtros.get('id_cancha') is not None:
        cond.append("id_cancha = :id_cancha")
        query_params["id_cancha"] = filtros["id_cancha"]


    if filtros.get('estado') is not None:
        cond.append("estado = :estado")
        query_params["estado"] = filtros["estado"]
    
    if filtros.get('fecha_desde') is not None:
        cond.append('DATE(fecha_hora_inicio) >= :fecha_desde')
        query_params['fecha_desde'] = filtros['fecha_desde']

    if filtros.get('fecha_hasta') is not None:
        cond.append('DATE(fecha_hora_inicio) <= :fecha_hasta')
        query_params['fecha_hasta'] = filtros['fecha_hasta']
        
    where = ""
    if len(cond) > 0:
        where = " Where "
        for condicion in range (len(cond)):
            where += cond[condicion]
            if condicion < len(cond) - 1: ## si no es el ultimo elemento de la lista, etra a este if
                where += ' AND '
    
    SQL = f"SELECT * FROM reservas {where} ORDER BY id ASC LIMIT :limit OFFSET :offset" #ordena por id de menor a mayor
    #cuando esta funcion recibe limit y offset como parámetros, ya le llegan validados y con su valor definitivo
    query_params["limit"] = limit
    query_params["offset"] = offset 
    
    return ejecutar_consulta(SQL, query_params) # sqlalchemy agarra :id_socio y lo relaciona con ej "id_socio": 5

def contar_reservas (filtros: dict) -> int:
    cond = [] 
    query_params = {}
    
# :algo es un parámetro que después se completa con el valor
# correspondiente dentro de query_params.
    
    if filtros.get('id_socio') is not None:
        cond.append("id_socio = :id_socio")
        query_params["id_socio"] = filtros["id_socio"]
    

    if filtros.get('id_cancha') is not None:
        cond.append("id_cancha = :id_cancha")
        query_params["id_cancha"] = filtros["id_cancha"]


    if filtros.get('estado') is not None:
        cond.append("estado = :estado")
        query_params["estado"] = filtros["estado"]
    
    if filtros.get('fecha_desde') is not None:
        cond.append('fecha_hora_inicio >= :fecha_desde')
        query_params['fecha_desde'] = filtros['fecha_desde']
        
    if filtros.get('fecha_hasta') is not None:
        cond.append('fecha_hora_inicio <=  :fecha_hasta')
        query_params['fecha_hasta'] = filtros['fecha_hasta']
        
    where = ""
    if len(cond) > 0:
        where = " Where "
        for condicion in range (len(cond)):
            where += cond[condicion]
            if condicion < len(cond) - 1: ## si no es el ultimo elemento de la lista, etra a este if
                where += ' AND '
    sql = "SELECT COUNT (*) as TOTAL from reservas" + where 
    
    filas = ejecutar_consulta (sql, query_params) #es una lista con un solo diccionario de la forma [{"total": valor}]
    return filas [0] ['total']
    
    
# funciones del metodo POST
def existe_superposicion_cancha(id_cancha: int, inicio, fin) -> bool:
    # Busca si la cancha ya tiene una reserva confirmada que se pise con el horario pedido.
    SQL = """
        SELECT 1 FROM reservas
        WHERE id_cancha = :id_cancha
          AND estado = 'confirmada'
          AND fecha_hora_inicio < :fin
          AND fecha_hora_fin > :inicio
        LIMIT 1
    """
    resultado = ejecutar_consulta(SQL, {
        "id_cancha": id_cancha,
        "inicio": inicio,
        "fin": fin,
    })
    return len(resultado) > 0

def existe_superposicion_socio(id_socio: int, inicio, fin) -> bool:
    # se fija que el socio no tenga otra reserva confirmada en el mismo horario
    SQL = """
        SELECT 1 FROM reservas
        WHERE id_socio = :id_socio
          AND estado = 'confirmada'
          AND fecha_hora_inicio < :fin
          AND fecha_hora_fin > :inicio
        LIMIT 1
    """
    resultado = ejecutar_consulta(SQL, {
        "id_socio": id_socio,
        "inicio": inicio,
        "fin": fin,
    })
    return len(resultado) > 0

def crear(datos: dict) -> dict:
    SQL = """
        INSERT INTO reservas
            (id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
        VALUES
            (:id_socio, :id_cancha, :fecha_hora_inicio, :fecha_hora_fin, :estado, :precio_hora, :precio_total)
    """
    # Se le saca la zona horaria a las fechas porque la collumna en la DB la tiene como datatime sin zona horaria GMT-3
    nuevo_id = ejecutar_escritura(SQL, {
        **datos,
        "fecha_hora_inicio": datos["fecha_hora_inicio"].replace(tzinfo=None),
        "fecha_hora_fin": datos["fecha_hora_fin"].replace(tzinfo=None),
    })

    return {
        "id": nuevo_id,
        "id_socio": datos["id_socio"],
        "id_cancha": datos["id_cancha"],
        "fecha_hora_inicio": _formatear_fecha(datos["fecha_hora_inicio"]),
        "fecha_hora_fin": _formatear_fecha(datos["fecha_hora_fin"]),
        "estado": datos["estado"],
        "precio_hora": datos["precio_hora"],
        "precio_total": datos["precio_total"],
    }
    
def _formatear_fecha(dt) -> str:
    # Convierte un datetime al formato de fecha GMT-3
    return dt.strftime(FORMATO_FECHA_HORA)
