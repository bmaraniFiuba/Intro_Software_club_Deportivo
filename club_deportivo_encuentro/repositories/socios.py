from club_deportivo_encuentro.db import ejecutar_consulta, ejecutar_escritura
from club_deportivo_encuentro.utils import cambiar_formato_booleano

def obtener_socios(filtros):
    """Obtiene socios filtrados y paginados, junto con el total sin paginar."""
    where = ' FROM socios WHERE 1=1'
    params = {}

    if filtros.get('nombre') is not None:
        where += ' AND LOWER(nombre) LIKE LOWER(:nombre)'
        params['nombre'] = f"%{filtros['nombre']}%"

    if filtros.get('activo') is not None:
        where += ' AND activo = :activo'
        params['activo'] = filtros['activo']

    total = ejecutar_consulta(
        'SELECT COUNT(*) AS total' + where,
        params,
    )[0]['total']

    params.update({
        'limit': filtros['_limit'],
        'offset': filtros['_offset'],
    })

    filas = ejecutar_consulta(
        'SELECT *' + where + ' ORDER BY id ASC LIMIT :limit OFFSET :offset',
        params,
    )

    return [cambiar_formato_booleano(fila) for fila in filas], total

def existe_email(email, id_socio=None):
    """Indica si el email ya pertenece a un socio."""
    sql = 'SELECT id FROM socios WHERE email = :email'
    params = {'email': email}

    if id_socio is not None:
        sql += ' AND id <> :id_socio'
        params['id_socio'] = id_socio

    filas = ejecutar_consulta(sql + ' LIMIT 1', params)
    return bool(filas)

def obtener_por_id(id_socio):
    """Obtiene un socio por id. Retorna None si no existe."""
    filas = ejecutar_consulta(
        'SELECT * FROM socios WHERE id = :id',
        {'id': id_socio},
    )

    return cambiar_formato_booleano(filas[0]) if filas else None