from sqlalchemy.exc import IntegrityError

from club_deportivo_encuentro.constants import ERROR_CODE_SOCIO_NOT_FOUND
from club_deportivo_encuentro.repositories import socios as repository
from club_deportivo_encuentro.utils import construir_error_api


ERROR_CODE_SOCIO_EMAIL_DUPLICADO = 'socio.email.duplicate'


def obtener_socios(filtros):
    return repository.obtener_socios(filtros)


def obtener_socio_por_id(id_socio):
    socio = repository.obtener_por_id(id_socio)
    if socio is None:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_SOCIO_NOT_FOUND,
            message='Socio no encontrado',
            description=f'No existe un socio con id {id_socio}',
        ), 404)
    return socio