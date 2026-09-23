from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from club_deportivo_encuentro.services import socios as service
from club_deportivo_encuentro.utils import construir_links, respuesta_paginada, validar_paginacion
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
    return

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
    return