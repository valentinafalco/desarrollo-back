from flask import Blueprint
from main.dominios.descripcionplaylist.controller_descripcionPlaylist import (
    crear_descripcion_playlist_controller,
    modificar_descripcion_playlist_controller,
    eliminar_descripcion_playlist_controller,
    listar_descripciones_playlist_controller,
    obtener_descripcion_playlist_controller
)

# Crear el blueprint para DescripcionPlaylist
descripcionplaylist_bp = Blueprint('descripcionplaylist_bp', __name__)

# -------------------- RUTAS DESCRIPCIÓN PLAYLIST --------------------

# Crear una descripción de playlist
@descripcionplaylist_bp.route('/descripciones_playlist', methods=['POST'])
def crear_descripcion_playlist():
    return crear_descripcion_playlist_controller()

# Listar todas las descripciones de playlist
@descripcionplaylist_bp.route('/descripciones_playlist', methods=['GET'])
def listar_descripciones_playlist():
    return listar_descripciones_playlist_controller()

# Obtener una descripción de playlist por ID
@descripcionplaylist_bp.route('/descripciones_playlist/<int:id>', methods=['GET'])
def obtener_descripcion_playlist(id):
    return obtener_descripcion_playlist_controller(id)

# Modificar una descripción de playlist existente
@descripcionplaylist_bp.route('/descripciones_playlist/<int:id>', methods=['PUT'])
def modificar_descripcion_playlist(id):
    return modificar_descripcion_playlist_controller(id)

# Eliminar una descripción de playlist
@descripcionplaylist_bp.route('/descripciones_playlist/<int:id>', methods=['DELETE'])
def eliminar_descripcion_playlist(id):
    return eliminar_descripcion_playlist_controller(id)