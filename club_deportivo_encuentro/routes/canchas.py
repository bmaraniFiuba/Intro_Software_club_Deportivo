from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from club_deportivo_encuentro.services import canchas as service
from club_deportivo_encuentro.validators import canchas as validator
from club_deportivo_encuentro.utils import construir_error_api, respuesta_paginada, validar_paginacion

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def listar_canchas():
    try:
        limit, offset = validar_paginacion(request.args)
        filtros = validator.validar_filtros_canchas(request.args)
    except ValueError as error:
        return jsonify(error.args[0]), 400

    filtros.update({'_limit': limit, '_offset': offset})
    try:
        canchas, total = service.obtener_canchas(filtros)
    except SQLAlchemyError:
        return jsonify(construir_error_api(
            'internal.error', 'Error interno del servidor', 'No se pudieron consultar las canchas.'
        )), 500
    return respuesta_paginada('canchas', canchas, total, limit, offset)

@canchas_bp.route('/canchas', methods=['POST'])
def crear_cancha():
    data = request.get_json()
    
    # validator.validar_creacion(data) # Descomentar cuando tengas el validador
    
    nueva_cancha = service.crear_cancha(data)
    return jsonify(nueva_cancha), 201


@canchas_bp.route('/canchas/<int:id>', methods=['GET'])
def obtener_cancha(id):
    cancha = service.obtener_cancha_por_id(id)
    return jsonify(cancha), 200


@canchas_bp.route('/canchas/<int:id>', methods=['PATCH'])
def actualizar_cancha(id):
    data = request.get_json()
    
    # validator.validar_actualizacion(data) # Descomentar cuando tengas el validador
    
    service.actualizar_cancha(id, data)
    return '', 204


@canchas_bp.route('/canchas/<int:id>', methods=['DELETE'])
def eliminar_cancha(id):
    service.eliminar_cancha(id)
    return '', 204


@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def listar_canchas_disponibles():
    params = {
        'fecha': request.args.get('fecha'),
        'hora_inicio': request.args.get('hora_inicio'),
        'hora_fin': request.args.get('hora_fin'),
        'id_deporte': request.args.get('id_deporte', type=int),
        'techada': request.args.get('techada', type=lambda v: v.lower() == 'true' if v else None),
        '_limit': request.args.get('_limit', default=10, type=int),
        '_offset': request.args.get('_offset', default=0, type=int)
    }
    
    # validator.validar_disponibilidad(params) # Descomentar cuando tengas el validador

    resultado = service.obtener_canchas_disponibles(params)
    
    if not resultado or not resultado.get('canchas'):
        return jsonify({'canchas': [], '_links': {}}), 200  # Ojo, el enunciado dice: "Si no hay canchas libres, responder 200 con un arreglo vacío"

    return jsonify(resultado), 200