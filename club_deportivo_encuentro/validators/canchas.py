from datetime import date, datetime
from re import fullmatch
from club_deportivo_encuentro.utils import construir_error_api, validar_entero_estricto
from club_deportivo_encuentro.constants import (DURACION_MAXIMA_HORAS, DURACION_MINIMA_HORAS, HORA_APERTURA, HORA_CIERRE, ZONA_GMT3,)


def _validar_datos_cancha(data, parcial):
    if not isinstance(data, dict):
        raise ValueError(construir_error_api('invalid.body', 'JSON inválido', 'El cuerpo debe ser un objeto JSON.'))
    errores = []
    
    # Permite 'id_deporte' en la creación (cuando parcial es False)
    campos_permitidos = ('nombre', 'precio_hora', 'techada', 'activa') if parcial else ('nombre', 'id_deporte', 'precio_hora', 'techada', 'activa')
    
    for campo in data:
        if campo not in campos_permitidos:
            if parcial:
                errores.append(f"El campo '{campo}' no se puede modificar.")
            else:
                errores.append(f"El campo '{campo}' no es un campo válido.")


    if not parcial or 'nombre' in data:
        nombre = data.get('nombre')
        if not isinstance(nombre, str) or not nombre.strip():
            errores.append("El campo 'nombre' es obligatorio y debe ser un texto no vacío.")
        elif len(nombre.strip()) > 30:
            errores.append("El campo 'nombre' no puede superar los 30 caracteres.")
    campos_enteros = ('precio_hora',) if parcial else ('id_deporte', 'precio_hora')
    for campo in campos_enteros:
        if not parcial or campo in data:
            valor = data.get(campo)
            if type(valor) is not int or not 1 <= valor <= 2147483647:
                errores.append(f"El campo '{campo}' debe ser un entero entre 1 y 2147483647.")
    for campo in ('techada', 'activa'):
        if campo in data and type(data[campo]) is not bool:
            errores.append(f"El campo '{campo}' debe ser booleano (true o false).")
    if errores:
        raise ValueError(construir_error_api('invalid.body', 'Datos inválidos', ' '.join(errores)))


def validar_creacion_cancha(data):
    _validar_datos_cancha(data, parcial=False)


def validar_actualizacion_cancha(data):
    _validar_datos_cancha(data, parcial=True)


def validar_filtros_canchas(parametros):
    filtros = {'nombre': parametros.get('nombre')}
    if 'id_deporte' in parametros:
        filtros['id_deporte'] = validar_entero_estricto(parametros['id_deporte'], 'id_deporte')
    for campo in ('techada', 'activa'):
        valor = parametros.get(campo)
        if valor is not None:
            if valor.lower() not in ('true', 'false'):
                raise ValueError(construir_error_api(
                    f'invalid.{campo}.format', 'Filtro inválido',
                    f"El parámetro '{campo}' debe ser true o false."
                ))
            filtros[campo] = valor.lower() == 'true'
    return filtros


def validar_disponibilidad(parametros):
    filtros = validar_filtros_canchas({
        campo: parametros[campo] for campo in ('id_deporte', 'techada') if campo in parametros
    })
    errores = []
    fecha = parametros.get('fecha', '')
    # Validación de formato de cadenas:
    if not fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', fecha):
        errores.append("'fecha' es obligatoria y debe tener formato YYYY-MM-DD.")
    else:
        try:
            date.fromisoformat(fecha)
        except ValueError:
            errores.append("'fecha' debe ser una fecha válida.")
    for campo in ('hora_inicio', 'hora_fin'):
        valor = parametros.get(campo, '')
        if not fullmatch(r'([01][0-9]|2[0-3]):00:00', valor):
            errores.append(f"'{campo}' es obligatorio y debe tener formato HH:00:00 (00 a 23).")
        filtros[campo] = valor
    if not errores and filtros['hora_inicio'] >= filtros['hora_fin']:
        errores.append('La hora de fin debe ser posterior a la hora de inicio.')

    # Validación de reglas de negocio:
    if not errores:
        inicio = datetime.strptime(f"{fecha} {filtros['hora_inicio']}", '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZONA_GMT3)
        fin = datetime.strptime(f"{fecha} {filtros['hora_fin']}", '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZONA_GMT3)

        if inicio <= datetime.now(ZONA_GMT3):
            errores.append('La fecha y hora de inicio deben ser futuras.')

        if inicio.hour < HORA_APERTURA or fin.hour > HORA_CIERRE:
            errores.append(f"El horario debe estar entre las {HORA_APERTURA:02d}:00 y las {HORA_CIERRE:02d}:00 hs.")

        duracion = (fin - inicio).total_seconds() / 3600
        if duracion < DURACION_MINIMA_HORAS or duracion > DURACION_MAXIMA_HORAS:
            errores.append(f"La duración debe ser entre {DURACION_MINIMA_HORAS} y {DURACION_MAXIMA_HORAS} horas.")

    if errores:
        raise ValueError(construir_error_api('invalid.parameters', 'Parámetros inválidos', ' '.join(errores)))
    filtros['fecha'] = fecha
    return filtros
