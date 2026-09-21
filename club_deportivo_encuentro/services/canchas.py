from club_deportivo_encuentro.repositories import canchas as repository


def obtener_canchas() -> list[dict]:
    """Coordina la obtención de canchas delegando el acceso a datos."""
    return repository.obtener_canchas()
