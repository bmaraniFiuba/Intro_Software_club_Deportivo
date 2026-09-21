from flask import Blueprint, request, jsonify, url_for

from services import socios as socios_service
from utils import construir_links

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def get_socios():
    return

@socios_bp.route('/socios', methods=['POST'])
def post_socio():
    return

@socios_bp.route('/socios/<int:id_socio>', methods=['GET'])
def get_socio_id(id_socio):
    return

@socios_bp.route('/socios/<int:id_socio>', methods=['PATCH'])
def patch_socio(id_socio):
    return