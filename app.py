# .\venv\Scripts\Activate.ps1 --> activar el entorno

from flask import Flask

app = Flask(__name__)

# Definimos la ruta/endpoint “/” (la raíz de nuestra API)
@app.route("/")

def index():
 return "¡Hola mundo!" # esta es la "response" (respuesta) del endpoint
# Configuramos el servidor Web para que se ejecute en el puerto 8080
if __name__ == '__main__':
 app.run(port=8080, debug=True)
