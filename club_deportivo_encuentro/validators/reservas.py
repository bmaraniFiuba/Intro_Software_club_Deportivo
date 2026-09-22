from datetime import datetime
from ..constants import (ZONA_GMT3, FORMATO_FECHA_HORA)
from ..utils import construir_error_api


def validar_y_convertir_fecha(fecha_texto, nombre_campo):
    """
    Valida que el string cumpla estrictamente con el formato ISO 8601 GMT-3.
    Retorna un objeto datetime si es válido.
    """
    try:
        # Convierte el string a fecha. Si le falta un dígito o tiene otra zona, falla automáticamente.
        fecha_obj = datetime.strptime(fecha_texto, FORMATO_FECHA_HORA)
    except (ValueError, TypeError):
        raise ValueError(construir_error_api(
            code=f'invalid.{nombre_campo}.format',
            message=f"Formato de '{nombre_campo}' inválido",
            description=f"'{nombre_campo}' debe tener formato YYYY-MM-DDTHH:MM:SS.ffffff-03:00",
        ), 400)
    return fecha_obj.replace(tzinfo=ZONA_GMT3)

def validar_entero_positivo(valor, nombre_campo):
    if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
        raise ValueError(construir_error_api(
            code=f'invalid.{nombre_campo}.format',
            message=f"Formato de '{nombre_campo}' inválido",
            description=f"'{nombre_campo}' debe ser un entero positivo",
        ), 400)
    return valor

def validar_body_crear_reserva(body):
    if not isinstance(body, dict) or not body:
        raise ValueError(construir_error_api(
            code='invalid.body',
            message='Cuerpo inválido',
            description='El cuerpo debe ser un objeto JSON no vacío',
        ), 400)

    campos_esperados = {"id_socio", "id_cancha", "fecha_hora_inicio", "fecha_hora_fin"}
    desconocidos = set(body.keys()) - campos_esperados
    if desconocidos:
        raise ValueError(construir_error_api(
            code='invalid.body',
            message='Campos no reconocidos',
            description=f"Campos no reconocidos: {', '.join(sorted(desconocidos))}",
        ), 400)

    faltantes = campos_esperados - set(body.keys())
    if faltantes:
        raise ValueError(construir_error_api(
            code='invalid.body',
            message='Faltan campos obligatorios',
            description=f"Faltan campos obligatorios: {', '.join(sorted(faltantes))}",
        ), 400)

    return {
        "id_socio": validar_entero_positivo(body["id_socio"], "id_socio"),
        "id_cancha": validar_entero_positivo(body["id_cancha"], "id_cancha"),
        "fecha_hora_inicio": validar_y_convertir_fecha(body["fecha_hora_inicio"], "fecha_hora_inicio"),
        "fecha_hora_fin": validar_y_convertir_fecha(body["fecha_hora_fin"], "fecha_hora_fin"),
    }


