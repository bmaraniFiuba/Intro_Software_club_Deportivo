## Integrantes
-Gaston Roberti 116174
-Leandro Piccicacco 116059
-Lucía Hernández Tamagno 116281
-Tiago Elias Melilli 116111
-Alexis Martin Blazek 115977
-Agustín Perata 115580
-Cristian Nahuel Daglio 116017
-Juan Francisco Skanata 116128
-Baltazar Marani 115983

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
#ver si la base esta corriendo
docker compose ps

#ver las tablas de la base
docker exec -i mysql-club mysql -u root -proot -e "SHOW TABLES FROM Club_Deportivo;"

#entrar al modo iteractivo para visualizar el contenido de las tablas
docker exec -it mysql-club mysql -u root -p ---> (ingresar root como contrasena)

#luego en el modo interactivo seleccionar
USE Club_Deportivo
SHOW TABLES;

#para ver el contenido de una tabla especifica:
SELECT * FROM <nombre de tabla>;


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
