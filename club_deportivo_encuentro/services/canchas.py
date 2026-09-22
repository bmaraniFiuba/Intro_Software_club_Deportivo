from club_deportivo_encuentro.repositories import canchas as repository


def obtener_canchas(filtros):
    return repository.obtener_canchas(filtros)
