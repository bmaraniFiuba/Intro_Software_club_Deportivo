from datetime import datetime
from re import fullmatch, sub
import logging
from urllib.parse import urlencode
from flask import jsonify, request
from .constants import (
    ERROR_CODE_INVALID_MIN_VALUE,
    ERROR_CODE_INVALID_MAX_VALUE,
    PARAMETRO_LIMIT,
    PARAMETRO_OFFSET,
    PAGINACION_LIMIT_DEFAULT,
    PAGINACION_LIMIT_MINIMO,
    PAGINACION_LIMIT_MAXIMO,
    PAGINACION_OFFSET_DEFAULT,
    PAGINACION_OFFSET_MINIMO
)

logger = logging.getLogger(__name__)


def construir_error_api(code: str, message: str, description: str, level: str = 'error') -> dict:
    """Construye un payload de error compatible con el resto de la API."""
    return {
        'errors': [{
            'code': code,
            'message': message,
            'level': level,
            'description': description
        }]
    }


def validar_formato_fecha(fecha: str, formato: str, nombre: str = 'fecha') -> datetime:
    try:
        return datetime.strptime(fecha, formato)
    except ValueError:
        logger.warning(f"Formato de fecha invalido: '{fecha}' no cumple el formato '{formato}'")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{fecha}' no cumple el formato esperado '{formato}'"
        ))


def validar_entero(numero, nombre: str = 'numero') -> int:
    valor = str(numero)
    valor_sin_letras = sub('[a-zA-Z]+', '', valor)

    try:
        return int(valor_sin_letras)
    except ValueError:
        logger.warning(f"Valor numerico invalido: '{numero}' no puede convertirse a entero")

        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{numero}' no puede convertirse a un numero entero"
        ))


def validar_minimo(valor: int, minimo: int, nombre: str) -> int:
    if valor < minimo:
        logger.warning(f"Valor por debajo del minimo: '{nombre}' es {valor}, minimo esperado {minimo}")

        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message='Valor por debajo del minimo permitido',
            description=f"El parametro '{nombre}' debe ser mayor o igual a {minimo}. Se recibio: {valor}"
        ))

    return valor


def validar_maximo(valor: int, maximo: int, nombre: str) -> int:
    if valor > maximo:
        logger.warning(f"Valor por encima del maximo: '{nombre}' es {valor}, maximo esperado {maximo}")

        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MAX_VALUE,
            message='Valor por encima del maximo permitido',
            description=f"El parametro '{nombre}' debe ser menor o igual a {maximo}. Se recibio: {valor}"
        ))

    return valor


def validar_string_no_vacio(valor, nombre: str) -> str:
    if valor is None or not str(valor).strip():
        raise ValueError(construir_error_api(
            code=f'required.{nombre}',
            message=f"Campo requerido: '{nombre}'",
            description=f"El campo '{nombre}' es obligatorio y no puede estar vacio"
        ))

    return str(valor).strip()

def validar_entero_estricto(valor, nombre: str) -> int:
    texto = str(valor).strip()
 
    if not fullmatch(r'[+-]?[0-9]+', texto):
        logger.warning(f"Valor numerico invalido: '{valor}' no es un entero para '{nombre}'")
 
        raise ValueError(construir_error_api(
            code=f"invalid.{nombre.lstrip('_')}.format",
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{valor}' no puede convertirse a un numero entero"
        ))
 
    return int(texto)
 
 
def construir_links(url_base: str, parametros: dict, total: int, limit: int, offset: int) -> dict:
    """Arma el objeto '_links' de HATEOAS para un listado paginado.
 
    url_base:   URL del recurso SIN query string (en Flask: request.base_url).
    parametros: query params originales como dict comun (en Flask: request.args.to_dict()),
                para que los filtros se conserven al navegar entre paginas.
    total:      cantidad de registros que cumplen los filtros (antes de paginar).
    limit/offset: valores ya validados de la pagina actual.
 
    _prev y _next se omiten cuando no existen. _last apunta al inicio de la ultima pagina.
    """
    ultimo_offset = ((total - 1) // limit) * limit if total > 0 else 0
 
    def enlace(nuevo_offset: int) -> dict:
        query = {**parametros, PARAMETRO_LIMIT: limit, PARAMETRO_OFFSET: nuevo_offset}
        return {'href': f'{url_base}?{urlencode(query)}'}
 
    links = {'_first': enlace(0)}
 
    if offset > 0:
        # min(...) evita apuntar mas alla de la ultima pagina si el offset pedido se paso del total
        links['_prev'] = enlace(min(max(offset - limit, 0), ultimo_offset))
 
    if offset + limit < total:
        links['_next'] = enlace(offset + limit)
 
    links['_last'] = enlace(ultimo_offset)
    return links
 
 
def validar_paginacion(parametros) -> tuple[int, int]:
    """Lee _limit y _offset de los query params y devuelve (limit, offset) ya validados.
 
    Si faltan usa los valores por defecto (10 y 0). Si son invalidos lanza ValueError
    con el payload de error de la API (mismo criterio que el resto de las validaciones).
    """
    limit = validar_entero_estricto(parametros.get(PARAMETRO_LIMIT, PAGINACION_LIMIT_DEFAULT), PARAMETRO_LIMIT)
    limit = validar_minimo(limit, PAGINACION_LIMIT_MINIMO, PARAMETRO_LIMIT)
    limit = validar_maximo(limit, PAGINACION_LIMIT_MAXIMO, PARAMETRO_LIMIT)
 
    offset = validar_entero_estricto(parametros.get(PARAMETRO_OFFSET, PAGINACION_OFFSET_DEFAULT), PARAMETRO_OFFSET)
    offset = validar_minimo(offset, PAGINACION_OFFSET_MINIMO, PARAMETRO_OFFSET)
 
    return limit, offset
 
 
def respuesta_paginada(clave: str, registros: list[dict], total: int, limit: int, offset: int):
    """Arma la respuesta HTTP de un listado paginado. Usarla al final de toda ruta de listado.
 
    - Si ningun registro cumple los filtros (total == 0): 204 sin cuerpo (asi lo define el swagger).
    - Si no: 200 con los datos bajo 'clave' (canchas, socios, reservas...) y los '_links' HATEOAS.
      Si el _offset pedido se paso del total, la lista viene vacia pero con links para volver.
    """
    if total == 0:
        return '', 204
 
    links = construir_links(request.base_url, request.args.to_dict(), total, limit, offset)
    return jsonify({clave: registros, '_links': links}), 200