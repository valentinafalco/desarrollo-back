from flask import Blueprint
from main.dominios.evento.controller_evento import (
    crear_evento_controller,
    modificar_evento_controller,
    eliminar_evento_controller,
    listar_eventos_controller,
    obtener_evento_controller
)

# Crear el blueprint para Evento
evento_bp = Blueprint('evento_bp', __name__)

# -------------------- RUTAS EVENTO --------------------

# Crear un evento
@evento_bp.route('/eventos', methods=['POST'])
def crear_evento():
    return crear_evento_controller()

# Listar todos los eventos
@evento_bp.route('/eventos', methods=['GET'])
def listar_eventos():
    return listar_eventos_controller()

# Obtener un evento por ID
@evento_bp.route('/eventos/<int:id>', methods=['GET'])
def obtener_evento(id):
    return obtener_evento_controller(id)

# Modificar un evento existente
@evento_bp.route('/eventos/<int:id>', methods=['PUT'])
def modificar_evento(id):
    return modificar_evento_controller(id)

# Eliminar un evento
@evento_bp.route('/eventos/<int:id>', methods=['DELETE'])
def eliminar_evento(id):
    return eliminar_evento_controller(id)