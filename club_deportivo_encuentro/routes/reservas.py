from flask import Blueprint, request, jsonify

from ..services.reservas import crear_reserva, cambiar_estado_reserva, obtener_reserva_por_id, obtener_reservas_services
from ..validators.reservas import validar_body_crear_reserva, validar_body_cambiar_estado, validar_filtros_reservas, validar_estado, validar_rago_fechas
from ..utils import validar_paginacion, respuesta_paginada
from ..repositories.reservas import obtener_reservas, contar_reservas



reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():
    """ cosas por hacer:
            - validar el limit y el offset que llegan en la request
            - validar los filtros: estado y fecha
            - algunos codigos de error ya se arrojan en
            - se arma la paginacion y se arman los links
            
        ideas de casos de test: 
            - probar con diferente combinaciones de filtros
            - probar con algun filtro invalido ej, estado, fecha_desde > fechas_hasta, limit > 100
    """
    try:
        estado = validar_estado(request.args.get('estado'))
        limit, offset = validar_paginacion(request.args)
        fecha_desde, fecha_hasta = validar_rago_fechas (request.args.get('fecha_desde'), request.args.get('fecha_hasta'))
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    filtros = {
        'id_cancha': request.args.get("id_cancha"),
        "id_socio" : request.args.get("id_socio"),
        "estado" : estado,
        "fecha_desde": fecha_desde,
        "fecha_hasta" : fecha_hasta
    }
    
    # reservas, total = obtener_reservas_services(filtros, limit, offset)  ----> no anda bien
    reservas = obtener_reservas(filtros,limit,offset) # los casilleros :algo obtienen su valor de filtros
    total = contar_reservas (filtros)

    return respuesta_paginada("reservas", reservas,total,limit,offset) #aca devuelvo codigo 200 o 204

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

#////
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

