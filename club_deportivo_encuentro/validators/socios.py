import re
from club_deportivo_encuentro.utils import (construir_error_api,
                                            validar_entero_estricto,
                                            validar_string_no_vacio
                                            )
from club_deportivo_encuentro.constants import ERROR_CODE_INVALID_BODY

FORMATO_EMAIL = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
CAMPOS_SOCIO_CREACION = {'nombre', 'email'}
CAMPOS_SOCIO_ACTUALIZACION = {'nombre', 'email', 'activo'}
CAMPOS_FILTRO_SOCIOS = {'nombre', 'activo', '_limit', '_offset'}

def validar_id_socio(id_socio):
    """Valida que el id del socio sea un entero positivo."""
    valor = validar_entero_estricto(id_socio, 'id')
    if valor <= 0:
        raise ValueError(construir_error_api(
            code='invalid.id.format',
            message="Formato de 'id' invalido",
            description='El identificador del socio debe ser un entero positivo',
        ))
    return valor

def validar_nombre(nombre_socio):
    return validar_string_no_vacio(nombre_socio, 'nombre')

def validar_email(email_socio):
    if validar_string_no_vacio(email_socio, 'email'):
        if not re.fullmatch(FORMATO_EMAIL, email_socio):
            raise ValueError(construir_error_api(
                code='invalid.email.format',
                message="Formato de 'email' invalido",
                description=f"El valor '{email_socio}' no cumple el formato esperado de email"
            ))
        else:
            return email_socio
    else:
        raise ValueError(construir_error_api(
            code='missing.email',
            message="El campo 'email' es obligatorio",
            description="El campo 'email' no puede estar vacio"
        ))

def validar_booleano_parametro(valor, nombre):
    """Valida un parametro booleano recibido por query string."""
    if valor.lower() not in ('true', 'false'):
        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El parametro '{nombre}' debe ser true o false",
        ))
    return valor.lower() == 'true'


def validar_body_crear_socio(body):
    """Valida el body del POST /socios y devuelve los datos normalizados."""
    if not isinstance(body, dict) or not body:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Cuerpo invalido',
            description='El cuerpo debe ser un objeto JSON no vacio',
        ))

    desconocidos = set(body) - CAMPOS_SOCIO_CREACION
    if desconocidos:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Campos no reconocidos',
            description=f"Campos no reconocidos: {', '.join(sorted(desconocidos))}",
        ))

    faltantes = CAMPOS_SOCIO_CREACION - set(body)
    if faltantes:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Faltan campos obligatorios',
            description=f"Faltan campos obligatorios: {', '.join(sorted(faltantes))}",
        ))

    return {
        'nombre': validar_nombre(body['nombre']),
        'email': validar_email(body['email']),
    }


def validar_body_actualizar_socio(body):
    """Valida el body del PATCH /socios/{id}."""
    if not isinstance(body, dict) or not body:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Cuerpo invalido',
            description='El cuerpo debe ser un objeto JSON no vacio',
        ))

    desconocidos = set(body) - CAMPOS_SOCIO_ACTUALIZACION
    if desconocidos:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Campos no reconocidos',
            description=f"Campos no reconocidos: {', '.join(sorted(desconocidos))}",
        ))

    datos = {}

    if 'nombre' in body:
        datos['nombre'] = validar_nombre(body['nombre'])

    if 'email' in body:
        datos['email'] = validar_email(body['email'])

    if 'activo' in body:
        if type(body['activo']) is not bool:
            raise ValueError(construir_error_api(
                code='invalid.activo.format',
                message="Formato de 'activo' invalido",
                description="El campo 'activo' debe ser booleano (true o false)",
            ))
        datos['activo'] = body['activo']

    return datos


def validar_filtros_socios(parametros):
    """Valida los filtros de GET /socios."""
    desconocidos = set(parametros.keys()) - CAMPOS_FILTRO_SOCIOS
    if desconocidos:
        raise ValueError(construir_error_api(
            code='invalid.parameters',
            message='Parametros no reconocidos',
            description=f"Parametros no reconocidos: {', '.join(sorted(desconocidos))}",
        ))

    filtros = {'nombre': parametros.get('nombre'), 'activo': None}

    if filtros['nombre'] is not None:
        filtros['nombre'] = validar_string_no_vacio(filtros['nombre'], 'nombre')

    if 'activo' in parametros:
        filtros['activo'] = validar_booleano_parametro(parametros['activo'], 'activo')

    return filtros