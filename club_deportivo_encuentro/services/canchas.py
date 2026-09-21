from club_deportivo_encuentro.repositories import canchas as repository


def obtener_canchas() -> list[dict]:
    """Coordina la obtención de canchas delegando el acceso a datos."""
    return repository.obtener_canchas()
from club_deportivo_encuentro.repositories import canchas as repo # modificar 
from club_deportivo_encuentro.constants import BASE_URL # Asumiendo que tenés esto

def obtener_canchas(filtros):
    canchas_db = repo.obtener_canchas(filtros)
    
    # Armamos la respuesta con HATEOAS para cumplir con el contrato
    # Podés implementar una función auxiliar que arme los _first, _next, etc.
    return {
        'canchas': canchas_db,
        '_links': {
            '_first': {'href': f"{BASE_URL}/canchas?_limit={filtros['_limit']}&_offset=0"},
            # Acá agregarías _next, _prev, etc., dependiendo de la cantidad total de registros
        }
    }