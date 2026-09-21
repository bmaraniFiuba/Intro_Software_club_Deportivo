import os
from dotenv import load_dotenv

load_dotenv()

# URL base de la API
BASE_URL = '/club_deportivo_encuentro'

# Formato de fecha esperado por la API
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%S.%f%z'



# Configuracion de la base de datos MySQL (levantada via docker-compose)
DB_HOST     = os.getenv('DB_HOST', 'localhost')
DB_PORT     = int(os.getenv('DB_PORT', '3306'))
DB_USER     = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME     = os.getenv('DB_NAME', 'facultad')
DB_URL      = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Codigos de error, obviamente cambiarlos
ERROR_CODE_INVALID_BODY        = 'invalid.body'
ERROR_CODE_INVALID_MIN_VALUE   = 'invalid.min.value'
ERROR_CODE_INVALID_MAX_VALUE   = 'invalid.max.value'
ERROR_CODE_ALUMNO_NOT_FOUND    = 'alumno.not.found'
ERROR_CODE_MATERIA_NOT_FOUND   = 'materia.not.found'

# Horarios de atención y duración
HORA_APERTURA = 8
HORA_CIERRE = 23
DURACION_MINIMA_HORAS = 1
DURACION_MAXIMA_HORAS = 3