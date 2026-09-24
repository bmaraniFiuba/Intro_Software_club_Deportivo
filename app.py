from flask import Flask, jsonify
from club_deportivo_encuentro.constants import BASE_URL
from club_deportivo_encuentro.utils import construir_error_api

# Se importan los blueprints
from club_deportivo_encuentro.routes.socios import socios_bp
from club_deportivo_encuentro.routes.deportes import deportes_bp
from club_deportivo_encuentro.routes.canchas import canchas_bp
from club_deportivo_encuentro.routes.reservas import reservas_bp

app = Flask(__name__)

# Se registran las rutas aplicando el prefijo base de la API
app.register_blueprint(socios_bp, url_prefix=BASE_URL)
app.register_blueprint(deportes_bp, url_prefix=BASE_URL)
app.register_blueprint(canchas_bp, url_prefix=BASE_URL)
app.register_blueprint(reservas_bp, url_prefix=BASE_URL)

# Función para probar que servidor esté activo
@app.route("/")
def ping():
    return jsonify({"mensaje": "API del Club Deportivo en línea"}), 200

# Maneja error si se ingresa URL que no existe
@app.errorhandler(404)
def manejar_404(error):
    return jsonify(construir_error_api(
        code='resource.not.found',
        message='Recurso no encontrado',
        description='La URL solicitada no existe.',
    )), 404

# Maneja error si se ingresa método HTTP inválido para esa ruta
@app.errorhandler(405)
def manejar_405(error):
    return jsonify(construir_error_api(
        code='method.not.allowed',
        message='Método no permitido',
        description='El método HTTP usado no está soportado para esta ruta.',
    )), 405

# Se enciende el servidor
app.run(host="0.0.0.0", port=8080, debug=True)