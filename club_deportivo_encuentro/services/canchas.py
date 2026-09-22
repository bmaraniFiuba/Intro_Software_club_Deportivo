from sqlalchemy.exc import IntegrityError
from club_deportivo_encuentro.utils import construir_error_api
from club_deportivo_encuentro.repositories import canchas as repository


def obtener_canchas(filtros):
    return repository.obtener_canchas(filtros)


def crear_cancha(data):
    error_deporte = construir_error_api('deporte.not.found', 'Deporte no encontrado', 'El deporte no existe.')
    if not repository.existe_deporte(data['id_deporte']):
        raise ValueError(error_deporte)
    datos = dict(data)
    datos['nombre'] = datos['nombre'].strip()
    try:
        return repository.crear_cancha(datos)
    except IntegrityError as error:
        # El deporte pudo eliminarse después de la consulta anterior.
        if getattr(error.orig, 'errno', None) == 1452:
            raise ValueError(error_deporte) from error
        raise


def obtener_cancha_por_id(id_cancha):
    cancha = repository.obtener_cancha_por_id(id_cancha)
    if cancha is None:
        raise ValueError(construir_error_api('cancha.not.found', 'Cancha no encontrada', 'La cancha no existe.'))
    return cancha


def actualizar_cancha(id_cancha, data):
    obtener_cancha_por_id(id_cancha)
    datos = dict(data)
    if 'nombre' in datos:
        datos['nombre'] = datos['nombre'].strip()
    repository.actualizar_cancha(id_cancha, datos)


def eliminar_cancha(id_cancha):
    obtener_cancha_por_id(id_cancha)
    error_reservas = construir_error_api('cancha.has.reservas', 'No se puede eliminar', 'La cancha tiene reservas asociadas.')
    if repository.tiene_reservas(id_cancha):
        raise ValueError(error_reservas)
    try:
        repository.eliminar_cancha(id_cancha)
    except IntegrityError as error:
        # La FK también impide borrar si se creó una reserva concurrentemente.
        if getattr(error.orig, 'errno', None) == 1451:
            raise ValueError(error_reservas) from error
        raise


def obtener_canchas_disponibles(params):
    return repository.obtener_canchas_disponibles(params)
