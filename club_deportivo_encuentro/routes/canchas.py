from flask import Blueprint, jsonify

# Pendiente: crear esta función en el service y habilitar el import.
# from club_deportivo_encuentro.services.canchas import obtener_canchas

canchas_bp = Blueprint('canchas', __name__)


@canchas_bp.route('/canchas', methods=['GET'])
def listar_canchas():
    # Después reemplazaremos esta lista provisional por la llamada al service:
    # canchas = obtener_canchas()
    canchas = []

    if not canchas:
        return '', 204

    return jsonify({'canchas': canchas}), 200
