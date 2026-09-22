from flask import Blueprint, request, jsonify
from ..services.reservas import crear_reserva
from ..validators.reservas import validar_body_crear_reserva



reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():
    return

@reservas_bp.route('/reservas', methods=['POST'])
def post_reserva():
    body = request.get_json(silent=True)

    try:
        datos = validar_body_crear_reserva(body)
        reserva = crear_reserva(
            datos["id_socio"], datos["id_cancha"],
            datos["fecha_hora_inicio"], datos["fecha_hora_fin"],
        )
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status

    return jsonify(reserva), 201

@reservas_bp.route('/reservas/<int:id_reserva>', methods=['GET'])
def get_reserva_id(id_reserva):
    return

@reservas_bp.route('/reservas/<int:id_reserva>', methods=['PUT'])
def put_reserva(id_reserva):
    return
