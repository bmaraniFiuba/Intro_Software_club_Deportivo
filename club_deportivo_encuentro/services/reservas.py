from datetime import datetime, timezone, timedelta
from club_deportivo_encuentro.errors import ReservaNoEncontradaError, ValidationError, ConflictoReservaError
from club_deportivo_encuentro.repositories import reservas as reservas_repo
from club_deportivo_encuentro.repositories import canchas as canchas_repo
from club_deportivo_encuentro.repositories import socios as socios_repo

# Zona horaria GMT-3 (Argentina)
GMT3 = timezone(timedelta(hours=-3))


def _validar_fechas(fecha_inicio: datetime, fecha_fin: datetime):
    """Validaciones básicas de horario según el enunciado."""
    ahora = datetime.now(GMT3)

    if fecha_inicio <= ahora:
        raise ValidationError("La reserva debe ser para una fecha/hora futura.")

    if fecha_inicio >= fecha_fin:
        raise ValidationError("La hora de inicio debe ser anterior a la de fin.")

    if fecha_inicio.minute != 0 or fecha_fin.minute != 0:
        raise ValidationError("Las reservas deben ser en horas en punto.")

    duracion = (fecha_fin - fecha_inicio).total_seconds() / 3600
    if duracion < 1 or duracion > 3:
        raise ValidationError("La reserva debe durar entre 1 y 3 horas.")

    if fecha_inicio.date() != fecha_fin.date():
        raise ValidationError("La reserva no puede cruzar la medianoche.")

    if fecha_inicio.hour < 8 or fecha_fin.hour > 23 or (fecha_fin.hour == 23 and fecha_fin.minute > 0):
        raise ValidationError("El horario debe ser entre las 08:00 y las 23:00 hs.")


def crear_reserva(id_socio: int, id_cancha: int, fecha_hora_inicio: str, fecha_hora_fin: str):
    # 1. Parsear fechas
    try:
        inicio = datetime.fromisoformat(fecha_hora_inicio)
        fin = datetime.fromisoformat(fecha_hora_fin)
    except Exception:
        raise ValidationError("Formato de fecha inválido. Usar ISO 8601 GMT-3.")

    # 2. Validar reglas de horario
    _validar_fechas(inicio, fin)

    # 3. Validar Socio
    socio = socios_repo.obtener_por_id(id_socio)
    if not socio:
        raise ReservaNoEncontradaError("El socio no existe.")
    if not socio.get("activo"):
        raise ValidationError("El socio está inactivo.")

    # 4. Validar Cancha
    cancha = canchas_repo.obtener_por_id(id_cancha)
    if not cancha:
        raise ReservaNoEncontradaError("La cancha no existe.")
    if not cancha.get("activa"):
        raise ValidationError("La cancha está inactiva.")

    # 5. Validar Superposiciones (Conflicto 409)
    if reservas_repo.existe_superposicion_cancha(id_cancha, inicio, fin):
        raise ConflictoReservaError("La cancha ya está ocupada en ese horario.")

    if reservas_repo.existe_superposicion_socio(id_socio, inicio, fin):
        raise ConflictoReservaError("El socio ya tiene otra reserva en ese horario.")

    # 6. Calcular importes
    horas = int((fin - inicio).total_seconds() // 3600)
    precio_hora = cancha["precio_hora"]
    precio_total = horas * precio_hora

    # 7. Guardar en BD
    return reservas_repo.crear({
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin,
        "estado": "confirmada",
        "precio_hora": precio_hora,
        "precio_total": precio_total
    })


def obtener_reserva_por_id(id_reserva: int):
    reserva = reservas_repo.obtener_por_id(id_reserva)
    if not reserva:
        raise ReservaNoEncontradaError("Reserva no encontrada.")
    return reserva


def cambiar_estado_reserva(id_reserva: int, nuevo_estado: str):
    reserva = obtener_reserva_por_id(id_reserva)
    estado_actual = reserva["estado"]

    # Si se pide el mismo estado, no hace nada y devuelve la reserva
    if estado_actual == nuevo_estado:
        return reserva

    ahora = datetime.now(GMT3)
    inicio = reserva["fecha_hora_inicio"]
    fin = reserva["fecha_hora_fin"]

    # Si vinieron como string desde la base de datos, los convertimos a datetime
    if isinstance(inicio, str):
        inicio = datetime.fromisoformat(inicio)
    if isinstance(fin, str):
        fin = datetime.fromisoformat(fin)

    # Regla 1: Confirmada -> Cancelada (solo si no empezó)
    if estado_actual == "confirmada" and nuevo_estado == "cancelada":
        if inicio <= ahora:
            raise ConflictoReservaError("No se puede cancelar una reserva que ya empezó o pasó.")
        reservas_repo.actualizar_estado(id_reserva, "cancelada")
        reserva["estado"] = "cancelada"
        return reserva

    # Regla 2: Confirmada -> Finalizada (solo si ya terminó)
    if estado_actual == "confirmada" and nuevo_estado == "finalizada":
        if ahora < fin:
            raise ConflictoReservaError("No se puede finalizar una reserva antes de su hora de fin.")
        reservas_repo.actualizar_estado(id_reserva, "finalizada")
        reserva["estado"] = "finalizada"
        return reserva

    # Cualquier otro cambio de estado es inválido
    raise ConflictoReservaError(f"Transición no permitida de {estado_actual} a {nuevo_estado}.")