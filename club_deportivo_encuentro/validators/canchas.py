from club_deportivo_encuentro.utils import construir_error_api, validar_entero_estricto


def validar_creacion_cancha(data):
    """
    Valida el cuerpo JSON para la creación/edición de una cancha.
    Alineado con el esquema SQL de la base de datos Club_Deportivo.
    """
    errores = []

    # 1. Verificar que se envíe un JSON válido
    if not isinstance(data, dict):
        return ["El cuerpo de la petición debe ser un objeto JSON."]

    # 2. Validar 'id_deporte' (Requerido, entero positivo)
    id_deporte = data.get('id_deporte')
    if id_deporte is None:
        errores.append("El campo 'id_deporte' es obligatorio.")
    elif not isinstance(id_deporte, int) or id_deporte <= 0:
        errores.append("El campo 'id_deporte' debe ser un número entero positivo.")

    # 3. Validar 'nombre' (Requerido, texto, máx 30 caracteres)
    nombre = data.get('nombre')
    if not nombre or not isinstance(nombre, str) or not nombre.strip():
        errores.append("El campo 'nombre' es obligatorio y debe ser un texto.")
    elif len(nombre.strip()) > 30:
        errores.append("El campo 'nombre' no puede superar los 30 caracteres.")

    # 4. Validar 'precio_hora' (Requerido, entero positivo)
    precio_hora = data.get('precio_hora')
    if precio_hora is None:
        errores.append("El campo 'precio_hora' es obligatorio.")
    elif not isinstance(precio_hora, int) or precio_hora <= 0:
        errores.append("El campo 'precio_hora' debe ser un número entero positivo mayor a 0.")

    # 5. Validar 'techada' (Opcional en JSON, pero si viene debe ser booleano)
    if 'techada' in data and not isinstance(data['techada'], bool):
        errores.append("El campo 'techada' debe ser booleano (true o false).")

    # 6. Validar 'activa' (Opcional en JSON, pero si viene debe ser booleano)
    if 'activa' in data and not isinstance(data['activa'], bool):
        errores.append("El campo 'activa' debe ser booleano (true o false).")

    return errores


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
