from club_deportivo__encuentro.db import ejecutar_consulta


def obtener_reservas (filtros: dict, offset:int, limit:int) -> list[dict]:
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
        cond.append('fecha_hora_inicio <= :fecha_hasta')
        query_params['fecha_hasta'] = filtros['fecha_hasta']
        
    where = ""
    if len(cond) > 0:
        where = " Where "
        for condicion in range (len(cond)):
            where += cond[condicion]
            if condicion < len(cond) - 1: ## si no es el ultimo elemento de la lista, etra a este if
                where += ' AND '
    
        SQL = f"SELECT * FROM reservas {where} ORDER BY id LIMIT :limit OFFSET :offset"
        #cuando esta funcion recibe limit y offset como parámetros, ya le llegan validados y con su valor definitivo
        query_params["limit"] = limit
        query_params["offset"] = offset 
    return (SQL, query_params) # sqlalchemy agarra :id_socio y lo relaciona con ej "id_socio": 5
    
                