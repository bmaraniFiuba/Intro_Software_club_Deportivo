from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from ..services.reservas import crear_reserva, cambiar_estado_reserva, obtener_reserva_por_id, obtener_reservas
from ..validators.reservas import validar_body_crear_reserva, validar_body_cambiar_estado, validar_filtros_reservas
from ..utils import validar_paginacion, respuesta_paginada



reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():
    try:
        limit, offset = validar_paginacion(request.args)
        filtros = validar_filtros_reservas(request.args)
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status
    reservas, total = obtener_reservas(filtros, limit, offset)
    return respuesta_paginada('reservas', reservas, total, limit, offset)

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
    try:
        reserva = obtener_reserva_por_id(id_reserva)
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status

    return jsonify(reserva), 200

@reservas_bp.route('/reservas/<int:id_reserva>/estado', methods=['PUT'])
def put_reserva_estado(id_reserva):
    body = request.get_json(silent=True)
    try:
        nuevo_estado = validar_body_cambiar_estado(body)
        reserva = cambiar_estado_reserva(id_reserva, nuevo_estado)
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status
    
    return jsonify(reserva), 200

