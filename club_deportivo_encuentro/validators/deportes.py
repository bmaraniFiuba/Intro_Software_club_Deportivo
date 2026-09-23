import logging
from club_deportivo_encuentro.utils import construir_error_api
from club_deportivo_encuentro.constants import ERROR_CODE_PARAMETRO_DESCONOCIDO

logger = logging.getLogger(__name__)

def validar_listado_deportes(parametros) -> None:
    
    if parametros:
        desconocidos = ", ".join(sorted(parametros.keys()))
        logger.warning(f"Parametros desconocidos en /deportes: {desconocidos}")
        
        raise ValueError(construir_error_api(
            code=ERROR_CODE_PARAMETRO_DESCONOCIDO,
            message='Parametros no permitidos',
            description=f"El endpoint /deportes no acepta parametros. Se recibio: {desconocidos}"
        ))