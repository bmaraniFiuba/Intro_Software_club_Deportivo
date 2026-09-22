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
    data = request.get_json(silent=True)
    validator.validar_creacion_cancha(data)
    nueva_cancha = service.crear_cancha(data)
    return jsonify(nueva_cancha), 201


@canchas_bp.route('/canchas/<int:id>', methods=['GET'])
def obtener_cancha(id):
    cancha = service.obtener_cancha_por_id(id)
    return jsonify(cancha), 200


@canchas_bp.route('/canchas/<int:id>', methods=['PATCH'])
def actualizar_cancha(id):
    data = request.get_json(silent=True)
    validator.validar_actualizacion_cancha(data)
    service.actualizar_cancha(id, data)
    return '', 204


@canchas_bp.route('/canchas/<int:id>', methods=['DELETE'])
def eliminar_cancha(id):
    service.eliminar_cancha(id)
    return '', 204


@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def listar_canchas_disponibles():
    limit, offset = validar_paginacion(request.args)
    params = validator.validar_disponibilidad(request.args)
    params.update({'_limit': limit, '_offset': offset})
    canchas, total = service.obtener_canchas_disponibles(params)
    return respuesta_paginada('canchas', canchas, total, limit, offset)


@canchas_bp.errorhandler(ValueError)
def manejar_error_datos(error):
    respuesta = error.args[0]
    codigo = respuesta['errors'][0]['code']
    estados = {'cancha.not.found': 404, 'deporte.not.found': 404, 'cancha.has.reservas': 409}
    return jsonify(respuesta), estados.get(codigo, 400)


@canchas_bp.errorhandler(SQLAlchemyError)
def manejar_error_db(error):
    return jsonify(construir_error_api(
        'internal.error', 'Error interno del servidor', 'No se pudo completar la operación.'
    )), 500
