import re
from club_deportivo_encuentro.utils import construir_error_api, validar_string_no_vacio

FORMATO_EMAIL = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

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