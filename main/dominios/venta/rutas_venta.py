from flask import Blueprint
from main.dominios.venta.controller_venta import (
    crear_venta_controller,
    modificar_venta_controller,
    eliminar_venta_controller,
    listar_ventas_controller,
    obtener_venta_controller
)

# Crear el blueprint para Venta
venta_bp = Blueprint('venta_bp', __name__)

# -------------------- RUTAS VENTA --------------------

# Crear una venta
@venta_bp.route('/ventas', methods=['POST'])
def crear_venta():
    return crear_venta_controller()

# Listar todas las ventas
@venta_bp.route('/ventas', methods=['GET'])
def listar_ventas():
    return listar_ventas_controller()

# Obtener una venta por ID
@venta_bp.route('/ventas/<int:id>', methods=['GET'])
def obtener_venta(id):
    return obtener_venta_controller(id)

# Modificar una venta existente
@venta_bp.route('/ventas/<int:id>', methods=['PUT'])
def modificar_venta(id):
    return modificar_venta_controller(id)

# Eliminar una venta
@venta_bp.route('/ventas/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    return eliminar_venta_controller(id)