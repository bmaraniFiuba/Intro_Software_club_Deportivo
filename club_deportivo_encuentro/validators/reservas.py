from datetime import datetime, timezone, timedelta

def validar_y_convertir_fecha(fecha_texto: str) -> datetime:
    """
    Valida que el string cumpla estrictamente con el formato ISO 8601 GMT-3.
    Retorna un objeto datetime si es válido, o lanza un ValueError si es inválido.
    """
    # El %f fuerza los 6 dígitos de fracción de segundo. 
    # El -03:00 final está escrito "en crudo" para rechazar cualquier otra zona.
    formato_exacto = "%Y-%m-%dT%H:%M:%S.%f-03:00"
    
    # Convierte el string a fecha. Si le falta un dígito o tiene otra zona, falla automáticamente.
    fecha_obj = datetime.strptime(fecha_texto, formato_exacto)
    
    # Le inyecta la zona horaria GMT-3 para que Python pueda hacer comparaciones precisas
    return fecha_obj.replace(tzinfo=ZONA_GMT3)
