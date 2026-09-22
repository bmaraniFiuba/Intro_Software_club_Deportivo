from club_deportivo_encuentro.db import ejecutar_consulta

def _formatear_cancha(row):
    """Convierte los TINYINT de MySQL a booleanos de Python para el JSON."""
    if not row:
        return None
    row['techada'] = bool(row['techada'])
    row['activa'] = bool(row['activa'])
    return row

def obtener_canchas(filtros):
    where = " FROM canchas WHERE 1=1"
    params = {}
    for campo in ('id_deporte', 'techada', 'activa'):
        if filtros.get(campo) is not None:
            where += f" AND {campo} = :{campo}"
            params[campo] = filtros[campo]
    if filtros.get('nombre') is not None:
        where += " AND LOWER(nombre) LIKE LOWER(:nombre)"
        params['nombre'] = f"%{filtros['nombre']}%"

    total = ejecutar_consulta("SELECT COUNT(*) AS total" + where, params)[0]['total']
    params.update({'limit': filtros['_limit'], 'offset': filtros['_offset']})
    filas = ejecutar_consulta(
        "SELECT *" + where + " ORDER BY id ASC LIMIT :limit OFFSET :offset", params
    )
    return [_formatear_cancha(fila) for fila in filas], total

def crear_cancha(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO canchas (id_deporte, nombre, precio_hora, techada, activa) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    techada = data.get('techada', False)
    activa = data.get('activa', True)

    cursor.execute(query, (
        data['id_deporte'],
        data['nombre'].strip(),
        data['precio_hora'],
        techada,
        activa
    ))
    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return obtener_cancha_por_id(new_id)

def obtener_cancha_por_id(id_cancha):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM canchas WHERE id = %s", (id_cancha,))
    fila = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return _formatear_cancha(fila)

def actualizar_cancha(id_cancha, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    campos = []
    params = []
    
    for key, value in data.items():
        campos.append(f"{key} = %s")
        params.append(value)

    if not campos:
        return

    params.append(id_cancha)
    query = f"UPDATE canchas SET {', '.join(campos)} WHERE id = %s"

    cursor.execute(query, tuple(params))
    conn.commit()
    
    cursor.close()
    conn.close()

def tiene_reservas(id_cancha):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_cancha = %s", (id_cancha,))
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return count > 0

def eliminar_cancha(id_cancha):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM canchas WHERE id = %s", (id_cancha,))
    conn.commit()
    
    cursor.close()
    conn.close()

def obtener_canchas_disponibles(params):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Formateamos los strings para que MySQL los interprete como DATETIME
    fecha_hora_inicio = f"{params['fecha']} {params['hora_inicio']}"
    fecha_hora_fin = f"{params['fecha']} {params['hora_fin']}"

    # Lógica de exclusión: Si hay una reserva 'confirmada' cuyo inicio es menor al fin solicitado 
    # y su fin es mayor al inicio solicitado, la cancha está ocupada.
    query = """
        SELECT c.* FROM canchas c
        WHERE c.activa = TRUE
        AND c.id NOT IN (
            SELECT r.id_cancha FROM reservas r
            WHERE r.estado = 'confirmada'
            AND r.fecha_hora_inicio < %s 
            AND r.fecha_hora_fin > %s
        )
    """
    sql_params = [fecha_hora_fin, fecha_hora_inicio]

    if params.get('id_deporte') is not None:
        query += " AND c.id_deporte = %s"
        sql_params.append(params['id_deporte'])
    
    if params.get('techada') is not None:
        query += " AND c.techada = %s"
        sql_params.append(params['techada'])

    query += " ORDER BY c.id ASC LIMIT %s OFFSET %s"
    sql_params.extend([params['_limit'], params['_offset']])

    cursor.execute(query, tuple(sql_params))
    filas = cursor.fetchall()

    cursor.close()
    conn.close()

    return [_formatear_cancha(fila) for fila in filas]