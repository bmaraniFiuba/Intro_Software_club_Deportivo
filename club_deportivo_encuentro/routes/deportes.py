from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from club_deportivo_encuentro.services import deportes as service
from club_deportivo_encuentro.utils import construir_error_api


deportes_bp = Blueprint("deportes", __name__)


@deportes_bp.route('/deportes', methods=['GET'])
def listar_deportes():
	try:
		return jsonify(service.obtener_deportes()), 200
	except SQLAlchemyError:
		return jsonify(construir_error_api(
			'internal.error',
			'Error interno del servidor',
			'No se pudieron consultar los deportes.'
		)), 500