from club_deportivo_encuentro.db import ejecutar_consulta, ejecutar_escritura

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

def existe_deporte(id_deporte):
    filas = ejecutar_consulta('SELECT id FROM deportes WHERE id = :id', {'id': id_deporte})
    return bool(filas)


def crear_cancha(data):
    nuevo_id = ejecutar_escritura(
        'INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) '
        'VALUES (:nombre, :id_deporte, :precio_hora, :techada, :activa)',
        {'nombre': data['nombre'], 'id_deporte': data['id_deporte'],
         'precio_hora': data['precio_hora'], 'techada': data.get('techada', False),
         'activa': data.get('activa', True)}
    )
    return obtener_cancha_por_id(nuevo_id)


def obtener_cancha_por_id(id_cancha):
    filas = ejecutar_consulta('SELECT * FROM canchas WHERE id = :id', {'id': id_cancha})
    return _formatear_cancha(filas[0]) if filas else None


def actualizar_cancha(id_cancha, data):
    campos = []
    params = {'id': id_cancha}
    for campo in ('nombre', 'precio_hora', 'techada', 'activa'):
        if campo in data:
            campos.append(f'{campo} = :{campo}')
            params[campo] = data[campo]
    if campos:
        ejecutar_escritura('UPDATE canchas SET ' + ', '.join(campos) + ' WHERE id = :id', params)


def tiene_reservas(id_cancha):
    filas = ejecutar_consulta('SELECT id FROM reservas WHERE id_cancha = :id LIMIT 1', {'id': id_cancha})
    return bool(filas)


def eliminar_cancha(id_cancha):
    ejecutar_escritura('DELETE FROM canchas WHERE id = :id', {'id': id_cancha})


def obtener_canchas_disponibles(params):
    where = """ FROM canchas c WHERE c.activa = TRUE AND NOT EXISTS (
        SELECT 1 FROM reservas r WHERE r.id_cancha = c.id AND r.estado = 'confirmada'
        AND r.fecha_hora_inicio < :fin AND r.fecha_hora_fin > :inicio
    )"""
    valores = {'inicio': f"{params['fecha']} {params['hora_inicio']}",
               'fin': f"{params['fecha']} {params['hora_fin']}"}
    for campo in ('id_deporte', 'techada'):
        if params.get(campo) is not None:
            where += f' AND c.{campo} = :{campo}'
            valores[campo] = params[campo]
    total = ejecutar_consulta('SELECT COUNT(*) AS total' + where, valores)[0]['total']
    valores.update({'limit': params['_limit'], 'offset': params['_offset']})
    filas = ejecutar_consulta(
        'SELECT c.*' + where + ' ORDER BY c.id ASC LIMIT :limit OFFSET :offset', valores
    )
    return [_formatear_cancha(fila) for fila in filas], total
