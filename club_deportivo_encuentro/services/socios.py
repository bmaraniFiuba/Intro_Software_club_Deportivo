from sqlalchemy.exc import IntegrityError

from club_deportivo_encuentro.constants import ERROR_CODE_SOCIO_NOT_FOUND
from club_deportivo_encuentro.repositories import socios as repository
from club_deportivo_encuentro.utils import construir_error_api


ERROR_CODE_SOCIO_EMAIL_DUPLICADO = 'socio.email.duplicate'


def obtener_socios(filtros):
    return repository.obtener_socios(filtros)

def crear_socio(data):
    error_email = construir_error_api(
        code=ERROR_CODE_SOCIO_EMAIL_DUPLICADO,
        message='Email ya registrado',
        description='El email indicado ya pertenece a un socio',
    )

    if repository.existe_email(data['email']):
        raise ValueError(error_email, 409)

    datos = dict(data)
    datos['activo'] = True

    try:
        return repository.crear_socio(datos)
    except IntegrityError as error:
        if getattr(error.orig, 'errno', None) == 1072:
            raise ValueError(error_email, 409) from error
        raise


def obtener_socio_por_id(id_socio):
    socio = repository.obtener_por_id(id_socio)
    if socio is None:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_SOCIO_NOT_FOUND,
            message='Socio no encontrado',
            description=f'No existe un socio con id {id_socio}',
        ), 404)
    return socio


def actualizar_socio(id_socio, data):
    obtener_socio_por_id(id_socio)  # 404 si no existe
    if 'email' in data and repository.existe_email(data['email'], id_socio):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_SOCIO_EMAIL_DUPLICADO,
            message='Email ya registrado',
            description='El email indicado ya pertenece a otro socio',
        ), 409)
    repository.actualizar_socio(id_socio, data)