from flask import Blueprint
from main.dominios.track.controller_track import (
    listar_tracks_controller,
    obtener_track_controller,
    crear_track_controller,
    modificar_track_controller,
    eliminar_track_controller
)

# Crear blueprint para agrupar rutas relacionadas con Track

track_bp = Blueprint('track', __name__)

# GET - Listar todos los tracks
@track_bp.route('/tracks', methods=['GET'])
def listar_tracks():
    return listar_tracks_controller()

# GET - Obtener un track por ID
@track_bp.route('/tracks/<int:id>', methods=['GET'])
def obtener_track(id):
    return obtener_track_controller(id)

# POST - Crear un nuevo track
@track_bp.route('/tracks', methods=['POST'])
def crear_track():
    return crear_track_controller()

# PUT - Modificar un track existente
@track_bp.route('/tracks/<int:id>', methods=['PUT'])
def modificar_track(id):
    return modificar_track_controller(id)

# DELETE - Eliminar un track
@track_bp.route('/tracks/<int:id>', methods=['DELETE'])
def eliminar_track(id):
    return eliminar_track_controller(id)

