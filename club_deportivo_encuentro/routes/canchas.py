from flask import Blueprint, jsonify

from club_deportivo_encuentro.services import canchas as service

canchas_bp = Blueprint('canchas', __name__)


@canchas_bp.route('/canchas', methods=['GET'])
def listar_canchas():
    canchas = service.obtener_canchas()

    if not canchas:
        return '', 204

    return jsonify({'canchas': canchas}), 200
