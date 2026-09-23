from datetime import datetime
from ..constants import (ZONA_GMT3, FORMATO_FECHA_HORA)
from ..constants import ERROR_CODE_INVALID_BODY, ERROR_CODE_ESTADO_INVALIDO, FORMATO_FECHA
from ..utils import construir_error_api, validar_formato_fecha


ESTADOS_VALIDOS = ["confirmada", "cancelada", "finalizada"]

def validar_estado (estado):
    
    if estado in None:
        return None
    
    if estado not in ESTADOS_VALIDOS:
        raise ValueError(construir_error_api(
            code= ERROR_CODE_ESTADO_INVALIDO,
            message= 'Introduzca un estado valido',
            description= "El estado no pertenece a 'ESTADOS_VALIDOS'"
            
        ), 400)
        
    return estado

def validar_rago_fechas (fecha_desde: str, fecha_hasta:str):
    fecha_desde_validada = None
    fecha_hasta_validada = None
    
    if fecha_desde is not None:
        fecha_desde_validada = validar_formato_fecha (fecha_desde, FORMATO_FECHA,'fecha_desde')
        
    if fecha_hasta is not None:
        fecha_hasta_validada = validar_formato_fecha (fecha_hasta, FORMATO_FECHA,'fecha_hasta')
    
    if fecha_desde is not None and fecha_hasta is not None:
        if fecha_desde_validada > fecha_hasta_validada:
            raise ValueError (construir_error_api (
                code= "invalid_rangoFechas",
                message= "el rango de fechas es invalido",
                description="la fecha_desde debe ser menor a la fecha_hasta"
            ), 400)
    return fecha_desde, fecha_hasta
        


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


#AGREGO(se puede reacomodar)

def validar_body_cambiar_estado(body):
    if not isinstance(body, dict) or not body:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Cuerpo inválido',
            description='El cuerpo debe ser un objeto JSON no vacío',
        ), 400)

    campos_esperados = {"estado"}
    desconocidos = set(body.keys()) - campos_esperados
    if desconocidos:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Campos no reconocidos',
            description=f"Campos no reconocidos: {', '.join(sorted(desconocidos))}",
        ), 400)

    if "estado" not in body:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Falta el campo obligatorio',
            description="Falta el campo obligatorio: estado",
        ), 400)

    nuevo_estado = body["estado"]

    if not isinstance(nuevo_estado, str) or nuevo_estado not in ESTADOS_VALIDOS: #Un estado desconocido va a tirar 400
        raise ValueError(construir_error_api(
            code=ERROR_CODE_ESTADO_INVALIDO,
            message='Estado desconocido',
            description=f"'estado' debe ser uno de: {', '.join(sorted(ESTADOS_VALIDOS))}",
        ), 400)

    return nuevo_estado
