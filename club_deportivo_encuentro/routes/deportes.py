from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from ..services import deportes as service
from ..validators import deportes as validator
from ..utils import construir_error_api
from ..constants import ERROR_CODE_INTERNAL


deportes_bp = Blueprint("deportes", __name__)


@deportes_bp.route('/deportes', methods=['GET'])
def listar_deportes():
    
    # Este endpoint no acepta query params por lo que si llega alguno, hay ValueError
    try:
        validator.validar_listado_deportes(request.args)
    except ValueError as error:
        return jsonify(error.args[0]), 400
    
    #
    try:
        deportes = service.obtener_deportes()
    except SQLAlchemyError:
        return jsonify(construir_error_api(
			code=ERROR_CODE_INTERNAL,
			message='Error interno del servidor',
			description='No se pudieron consultar los deportes.'
		)), 500
    
    # Si la tabla esta vacia, devuelve 204 No Content
    if not deportes:
        return '', 204
    
    return jsonify({'deportes': deportes}), 200