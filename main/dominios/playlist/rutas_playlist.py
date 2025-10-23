from flask import Blueprint
from main.dominios.playlist.controller_playlist import (
    crear_playlist_controller,
    modificar_playlist_controller,
    eliminar_playlist_controller,
    listar_playlists_controller,
    obtener_playlist_controller
)

# Crear el blueprint para Playlist
playlist_bp = Blueprint('playlist_bp', __name__)

# -------------------- RUTAS PLAYLIST --------------------

# Crear una playlist
@playlist_bp.route('/playlists', methods=['POST'])
def crear_playlist():
    return crear_playlist_controller()

# Listar todas las playlists
@playlist_bp.route('/playlists', methods=['GET'])
def listar_playlists():
    return listar_playlists_controller()

# Obtener una playlist por ID
@playlist_bp.route('/playlists/<int:id>', methods=['GET'])
def obtener_playlist(id):
    return obtener_playlist_controller(id)

# Modificar una playlist existente
@playlist_bp.route('/playlists/<int:id>', methods=['PUT'])
def modificar_playlist(id):
    return modificar_playlist_controller(id)

# Eliminar una playlist
@playlist_bp.route('/playlists/<int:id>', methods=['DELETE'])
def eliminar_playlist(id):
    return eliminar_playlist_controller(id)