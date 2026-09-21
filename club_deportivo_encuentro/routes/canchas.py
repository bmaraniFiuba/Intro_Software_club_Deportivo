from flask import Blueprint, jsonify, request
from club_deportivo_encuentro.services import canchas as service
# Agregar validardores  club_deportivo_encuentro.validators import canchas as validator

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def listar_canchas():
    # 1. Capturar filtros y paginación desde la query string
    filtros = {
        'id_deporte': request.args.get('id_deporte', type=int),
        'nombre': request.args.get('nombre', type=str),
        'techada': request.args.get('techada', type=lambda v: v.lower() == 'true' if v else None),
        'activa': request.args.get('activa', type=lambda v: v.lower() == 'true' if v else None),
        '_limit': request.args.get('_limit', default=10, type=int),
        '_offset': request.args.get('_offset', default=0, type=int)
    }

    # 2. Pasar los filtros al servicio
    resultado = service.obtener_canchas(filtros)

    # 3. Responder 204 si la lista de canchas está vacía
    if not resultado or not resultado.get('canchas'):
        return '', 204

    # 4. Retornar JSON (el servicio ya debería devolver el diccionario con 'canchas' y '_links')
    return jsonify(resultado), 200


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