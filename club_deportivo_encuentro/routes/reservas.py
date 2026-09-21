from flask import Blueprint, request, jsonify, url_for


reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():
    return

@reservas_bp.route('/reservas', methods=['POST'])
def post_reserva():
    return

@reservas_bp.route('/reservas/<int:id_socio>', methods=['GET'])
def get_reserva_id():
    return

@reservas_bp.route('/reservas/<int:id_socio>', methods=['PATCH'])
def put_reserva():
    return
