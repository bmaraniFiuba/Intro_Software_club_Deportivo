from datetime import datetime
from ..repositories import reservas as reservas_repo
from ..repositories import canchas as canchas_repo
from ..repositories import socios as socios_repo
from ..constants import (
    ZONA_GMT3, HORA_APERTURA, HORA_CIERRE,
    DURACION_MINIMA_HORAS, DURACION_MAXIMA_HORAS,
    ESTADO_CONFIRMADA, ESTADO_CANCELADA, ESTADO_FINALIZADA,
    ERROR_CODE_SOCIO_NOT_FOUND, ERROR_CODE_CANCHA_NOT_FOUND,
    ERROR_CODE_RESERVA_NOT_FOUND, ERROR_CODE_TRANSICION_INVALIDA,
)
from ..utils import construir_error_api


def asegurar_aware_datetime(fecha):
    #Convierte a datetime aware en GMT-3, venga como string o como datetime naive
    if isinstance(fecha, str):
        fecha = datetime.fromisoformat(fecha)
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=ZONA_GMT3)
    return fecha.astimezone(ZONA_GMT3)

def _validar_fechas(fecha_inicio: datetime, fecha_fin: datetime):
    """Validaciones básicas de horario según el enunciado."""
    ahora = datetime.now(ZONA_GMT3)

    if fecha_inicio <= ahora:
        raise ValueError(construir_error_api(
            code='fecha.pasada',
            message='Fecha inválida',
            description='La reserva debe ser para una fecha/hora futura',
        ), 400)

    if fecha_inicio >= fecha_fin:
        raise ValueError(construir_error_api(
            code='intervalo.invalido',
            message='Intervalo inválido',
            description='La hora de inicio debe ser anterior a la de fin',
        ), 400)

    if (fecha_inicio.minute, fecha_inicio.second, fecha_inicio.microsecond) != (0, 0, 0):
        raise ValueError(construir_error_api(
            code='horario.invalido',
            message='Horario inválido',
            description='La hora de inicio debe ser en punto',
        ), 400)
    
    if (fecha_fin.minute, fecha_fin.second, fecha_fin.microsecond) != (0, 0, 0):
        raise ValueError(construir_error_api(
            code='horario.invalido',
            message='Horario inválido',
            description='La hora de fin debe ser en punto',
        ), 400)

    duracion = (fecha_fin - fecha_inicio).total_seconds() / 3600
    if duracion < DURACION_MINIMA_HORAS or duracion > DURACION_MAXIMA_HORAS:
        raise ValueError(construir_error_api(
            code='duracion.invalida',
            message='Duración inválida',
            description=f"La reserva debe durar entre {DURACION_MINIMA_HORAS} y {DURACION_MAXIMA_HORAS} horas",
        ), 400)

    if fecha_inicio.date() != fecha_fin.date():
        raise ValueError(construir_error_api(
            code='cruza.medianoche',
            message='Intervalo inválido',
            description='La reserva no puede cruzar la medianoche',
        ), 400)

    if fecha_inicio.hour < HORA_APERTURA or fecha_fin.hour > HORA_CIERRE:
        raise ValueError(construir_error_api(
            code='fuera.de.horario',
            message='Horario inválido',
            description=f"El horario debe ser entre las {HORA_APERTURA:02d}:00 y las {HORA_CIERRE:02d}:00 hs",
        ), 400)


def crear_reserva(id_socio: int, id_cancha: int, fecha_hora_inicio: str, fecha_hora_fin: str):    
    fecha_hora_inicio = asegurar_aware_datetime(fecha_hora_inicio)
    fecha_hora_fin = asegurar_aware_datetime(fecha_hora_fin)
    
    # 1. Validar reglas de horario
    _validar_fechas(fecha_hora_inicio, fecha_hora_fin)

    # 2. Validar Socio
    socio = socios_repo.obtener_por_id(id_socio)
    if not socio:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_SOCIO_NOT_FOUND,
            message='Socio no encontrado',
            description=f"No existe un socio con id {id_socio}",
        ), 404)
    if not socio.get("activo"):
        raise ValueError(construir_error_api(
            code='socio.inactivo',
            message='Socio inactivo',
            description='El socio está inactivo y no puede reservar',
        ), 409)

    # 3. Validar Cancha
    cancha = canchas_repo.obtener_cancha_por_id(id_cancha)
    if not cancha:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_CANCHA_NOT_FOUND,
            message='Cancha no encontrada',
            description=f"No existe una cancha con id {id_cancha}",
        ), 404)
    if not cancha.get("activa"):
        raise ValueError(construir_error_api(
            code='cancha.inactiva',
            message='Cancha inactiva',
            description='La cancha está inactiva y no admite reservas',
        ), 409)

    # 4. Validar Superposiciones (Conflicto 409)
    if reservas_repo.existe_superposicion_cancha(id_cancha, fecha_hora_inicio, fecha_hora_fin):
        raise ValueError(construir_error_api(
            code='cancha.no.disponible',
            message='Cancha no disponible',
            description='La cancha ya está ocupada en ese horario',
        ), 409)

    if reservas_repo.existe_superposicion_socio(id_socio, fecha_hora_inicio, fecha_hora_fin):
        raise ValueError(construir_error_api(
            code='socio.no.disponible',
            message='Socio no disponible',
            description='El socio ya tiene otra reserva en ese horario',
        ), 409)

    # 5. Calcular importes
    horas = int((fecha_hora_fin - fecha_hora_inicio).total_seconds() // 3600)
    precio_hora = cancha["precio_hora"]
    precio_total = horas * precio_hora

    # 6. Guardar en BD
    return reservas_repo.crear({
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
        "estado": ESTADO_CONFIRMADA,
        "precio_hora": precio_hora,
        "precio_total": precio_total
    })


def obtener_reserva_por_id(id_reserva: int):
    reserva = reservas_repo.obtener_por_id(id_reserva)
    if not reserva:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_RESERVA_NOT_FOUND,
            message='Reserva no encontrada',
            description=f"No existe una reserva con id {id_reserva}",
        ), 404)
    return reserva

def obtener_reservas(filtros: dict, limit: int, offset: int):
    total = reservas_repo.contar_reservas(filtros)
    reservas = reservas_repo.obtener_reservas(filtros, limit=limit, offset=offset)
    return reservas, total

def obtener_reservas_services(filtros, limit, offset):
    reservas, total = obtener_reservas(filtros, limit, offset)
    return reservas, total


def cambiar_estado_reserva(id_reserva: int, nuevo_estado: str):
    reserva = obtener_reserva_por_id(id_reserva)
    estado_actual = reserva["estado"]

    # Si se pide el mismo estado, no hace nada y devuelve la reserva
    if estado_actual == nuevo_estado:
        return reserva

    ahora = datetime.now(ZONA_GMT3)
    inicio = asegurar_aware_datetime(reserva["fecha_hora_inicio"])
    fin = asegurar_aware_datetime(reserva["fecha_hora_fin"])

    
     # Regla 1: Confirmada -> Cancelada (solo si no empezó)
    if estado_actual == ESTADO_CONFIRMADA and nuevo_estado == ESTADO_CANCELADA:
        if inicio <= ahora:
            raise ValueError(construir_error_api(
                code=ERROR_CODE_TRANSICION_INVALIDA,
                message='Transición no permitida',
                description='No se puede cancelar una reserva que ya empezó o pasó',
            ), 409)
        reservas_repo.actualizar_estado(id_reserva, ESTADO_CANCELADA)
        reserva["estado"] = ESTADO_CANCELADA
        return reserva

    # Regla 2: Confirmada -> Finalizada (solo si ya terminó)
    if estado_actual == ESTADO_CONFIRMADA and nuevo_estado == ESTADO_FINALIZADA:
        if ahora < fin:
            raise ValueError(construir_error_api(
                code=ERROR_CODE_TRANSICION_INVALIDA,
                message='Transición no permitida',
                description='No se puede finalizar una reserva antes de su hora de fin',
            ), 409)
        reservas_repo.actualizar_estado(id_reserva, ESTADO_FINALIZADA)
        reserva["estado"] = ESTADO_FINALIZADA
        return reserva

    # Cualquier otro cambio de estado es inválido
    raise ValueError(construir_error_api(
        code=ERROR_CODE_TRANSICION_INVALIDA,
        message='Transición no permitida',
        description=f"Transición no permitida de {estado_actual} a {nuevo_estado}",
    ), 409)
