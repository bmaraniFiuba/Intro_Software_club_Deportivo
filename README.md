## Requisitos previos

* Tener instalado Docker y Docker Compose en el equipo.

---

## 1. Base de datos (Docker)

```bash
# Iniciar el contenedor en segundo plano
docker-compose up -d

# Detener el contenedor
docker-compose down
```

---

## 2. Configuración inicial del entorno

> **Nota:** Ejecutar este paso una única vez al clonar el repositorio o inicializar el proyecto.

### Opción A: Con virtualenv

* **Windows:**
  ```cmd
  setup_virtualenv.bat
  ```

* **Linux / macOS:**
  ```bash
  chmod +x setup_virtualenv.sh
  ./setup_virtualenv.sh
  ```

### Opción B: Con pipenv

* **Windows:**
  ```cmd
  setup_pipenv.bat
  ```

* **Linux / macOS:**
  ```bash
  chmod +x setup_pipenv.sh
  ./setup_pipenv.sh
  ```

---

## 3. Activar y desactivar el entorno virtual

Para trabajar en futuras sesiones:

### Con virtualenv

* **Activar en Windows:**
  ```cmd
  .venv\Scripts\activate
  ```

* **Activar en Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

* **Desactivar (cualquier SO):**
  ```bash
  deactivate
  ```

### Con pipenv

* **Activar en Windows:**
  ```cmd
  python -m pipx run pipenv shell
  ```

* **Activar en Linux / macOS:**
  ```bash
  pipenv shell
  ```

* **Desactivar (cualquier SO):**
  ```bash
  exit
  ```

---

## 4. Ejecutar la aplicación Flask

Con la base de datos levantada y el entorno configurado:

### Usando virtualenv (con el entorno activado)

* **Windows / Linux / macOS:**
  ```bash
  python app.py
  ```

### Usando pipenv

* **Windows:**
  ```cmd
  python -m pipx run pipenv run python app.py
  ```

* **Linux / macOS:**
  ```bash
  pipenv run python app.py
  ```