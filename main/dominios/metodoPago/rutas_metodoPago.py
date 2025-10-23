from flask import Blueprint
from main.dominios.metodoPago.controller_metodoPago import (
    crear_metodo_pago_controller,
    modificar_metodo_pago_controller,
    eliminar_metodo_pago_controller,
    listar_metodos_pago_controller,
    obtener_metodo_pago_controller
)

# Crear el blueprint para MetodoPago_Usuario
metodopago_bp = Blueprint('metodopago_bp', __name__)

# -------------------- RUTAS MÉTODO DE PAGO --------------------

# Crear un método de pago
@metodopago_bp.route('/metodos_pago', methods=['POST'])
def crear_metodo_pago():
    return crear_metodo_pago_controller()

# Listar todos los métodos de pago
@metodopago_bp.route('/metodos_pago', methods=['GET'])
def listar_metodos_pago():
    return listar_metodos_pago_controller()

# Obtener un método de pago por ID
@metodopago_bp.route('/metodos_pago/<int:id>', methods=['GET'])
def obtener_metodo_pago(id):
    return obtener_metodo_pago_controller(id)

# Modificar un método de pago existente
@metodopago_bp.route('/metodos_pago/<int:id>', methods=['PUT'])
def modificar_metodo_pago(id):
    return modificar_metodo_pago_controller(id)

# Eliminar un método de pago
@metodopago_bp.route('/metodos_pago/<int:id>', methods=['DELETE'])
def eliminar_metodo_pago(id):
    return eliminar_metodo_pago_controller(id)