from flask import Blueprint
from main.dominios.publicaciones.controller_publicacionEvento import (
    crear_publicacion_evento_controller,
    modificar_publicacion_evento_controller,
    eliminar_publicacion_evento_controller,
    listar_publicaciones_evento_controller,
    obtener_publicacion_evento_controller
)

publicacion_evento_bp = Blueprint('publicacion_evento_bp', __name__)

# Crear
@publicacion_evento_bp.route('/publicacionesEvento', methods=['POST'])
def crear_publicacion_evento():
    return crear_publicacion_evento_controller()

# Listar
@publicacion_evento_bp.route('/publicacionesEvento', methods=['GET'])
def listar_publicaciones_evento():
    return listar_publicaciones_evento_controller()

# Obtener por ID
@publicacion_evento_bp.route('/publicacionesEvento/<int:id>', methods=['GET'])
def obtener_publicacion_evento(id):
    return obtener_publicacion_evento_controller(id)

# Modificar
@publicacion_evento_bp.route('/publicacionesEvento/<int:id>', methods=['PUT'])
def modificar_publicacion_evento(id):
    return modificar_publicacion_evento_controller(id)

# Eliminar
@publicacion_evento_bp.route('/publicacionesEvento/<int:id>', methods=['DELETE'])
def eliminar_publicacion_evento(id):
    return eliminar_publicacion_evento_controller(id)
