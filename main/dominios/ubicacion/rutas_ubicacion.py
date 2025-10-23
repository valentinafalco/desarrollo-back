from flask import Blueprint
from main.dominios.ubicacion.controller_ubicacion import (
    crear_ubicacion_controller,
    modificar_ubicacion_controller,
    eliminar_ubicacion_controller,
    listar_ubicaciones_controller,
    obtener_ubicacion_controller
)

# Crear el blueprint para Ubicación
ubicacion_bp = Blueprint('ubicacion_bp', __name__)

# -------------------- RUTAS UBICACIÓN --------------------

# Crear una ubicación
@ubicacion_bp.route('/ubicaciones', methods=['POST'])
def crear_ubicacion():
    return crear_ubicacion_controller()

# Listar todas las ubicaciones
@ubicacion_bp.route('/ubicaciones', methods=['GET'])
def listar_ubicaciones():
    return listar_ubicaciones_controller()

# Obtener una ubicación por ID
@ubicacion_bp.route('/ubicaciones/<int:id>', methods=['GET'])
def obtener_ubicacion(id):
    return obtener_ubicacion_controller(id)

# Modificar una ubicación existente
@ubicacion_bp.route('/ubicaciones/<int:id>', methods=['PUT'])
def modificar_ubicacion(id):
    return modificar_ubicacion_controller(id)

# Eliminar una ubicación
@ubicacion_bp.route('/ubicaciones/<int:id>', methods=['DELETE'])
def eliminar_ubicacion(id):
    return eliminar_ubicacion_controller(id)