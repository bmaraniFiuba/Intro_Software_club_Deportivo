from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from club_deportivo_encuentro.services import socios as service
from club_deportivo_encuentro.utils import (construir_error_api,
                                            respuesta_paginada,
                                             validar_paginacion)
from club_deportivo_encuentro.constants import ERROR_CODE_INTERNAL
from club_deportivo_encuentro.validators import socios as validator

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def get_socios():
    try:
        limit, offset = validar_paginacion(request.args)
        filtros = validator.validar_filtros_socios(request.args)
    except ValueError as error:
        return jsonify(error.args[0]), 400

    filtros.update({'_limit': limit, '_offset': offset})
    socios, total = service.obtener_socios(filtros)

    return respuesta_paginada('socios', socios, total, limit, offset)

@socios_bp.route('/socios', methods=['POST'])
def post_socio():
    data = request.get_json(silent=True)

    try:
        data = validator.validar_body_crear_socio(data)
        socio = service.crear_socio(data)
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status

    return jsonify(socio), 201

@socios_bp.route('/socios/<int:id_socio>', methods=['GET'])
def get_socio_id(id_socio):
    try:
        id_socio = validator.validar_id_socio(id_socio)
        socio = service.obtener_socio_por_id(id_socio)
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status

    return jsonify(socio), 200

@socios_bp.route('/socios/<int:id_socio>', methods=['PATCH'])
def patch_socio(id_socio):
    try:
        id_socio = validator.validar_id_socio(id_socio)
        data = request.get_json(silent=True)
        data = validator.validar_body_actualizar_socio(data)
        service.actualizar_socio(id_socio, data)
    except ValueError as error:
        status = error.args[1] if len(error.args) > 1 else 400
        return jsonify(error.args[0]), status
    return '', 204

@socios_bp.errorhandler(SQLAlchemyError)
def manejar_error_db(error):
    return jsonify(construir_error_api(
        code=ERROR_CODE_INTERNAL,
        message='Error interno del servidor',
        description='No se pudo completar la operación.',
    )), 500