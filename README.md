## Requisitos previos

* Tener instalado Docker y Docker Compose en el equipo. para usar la DB con docker-compose

---

## 1. Base de datos (Docker)

Comandos para gestionar el contenedor de la base de datos:

# Iniciar el contenedor
docker-compose up -d

# Detener el contenedor
docker-compose down

---

## 2. Configuración inicial del entorno

Nota: Ejecutar este paso una única vez al clonar el repositorio o inicializar el proyecto.

### Opción A: Con virtualenv

* Windows:
  setup_virtualenv.bat

* Linux / macOS:
  chmod +x setup_virtualenv.sh
  ./setup_virtualenv.sh

### Opción B: Con pipenv

* Windows:
  setup_pipenv.bat

* Linux / macOS:
  chmod +x setup_pipenv.sh
  ./setup_pipenv.sh

---

## 3. Activar y desactivar el entorno virtual

Para trabajar en futuras sesiones:

### Con virtualenv

* Activar en Windows:
  .venv\Scripts\activate

* Activar en Linux / macOS:
  source .venv/bin/activate

* Desactivar (cualquier SO):
  deactivate

### Con pipenv

* Activar en Windows:
  python -m pipx run pipenv shell

* Activar en Linux / macOS:
  pipenv shell

* Desactivar (cualquier SO):
  exit

---

## 4. Ejecutar la aplicación Flask

Con la base de datos levantada y el entorno configurado:

### Usando virtualenv (con el entorno activado)

* Windows / Linux / macOS:
  python app.py

### Usando pipenv

* Windows:
  python -m pipx run pipenv run python app.py

* Linux / macOS:
  pipenv run python app.py