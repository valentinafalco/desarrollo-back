from flask import Blueprint, request
from main.dominios.compra.controller_compra import (
    listar_compras_controller,
    obtener_compra_controller,
    crear_compra_controller,
    modificar_compra_controller,
    eliminar_compra_controller
)

compra_bp = Blueprint('compra', __name__)

@compra_bp.route('/compras', methods=['GET'])
def listar_compras():
    return listar_compras_controller()

@compra_bp.route('/compras/<int:id>', methods=['GET'])
def obtener_compra(id):
    return obtener_compra_controller(id)

@compra_bp.route('/compras', methods=['POST'])
def crear_compra():
    data = request.get_json()
    return crear_compra_controller(data)

@compra_bp.route('/compras/<int:id>', methods=['PUT'])
def modificar_compra(id):
    data = request.get_json()
    return modificar_compra_controller(id, data)

@compra_bp.route('/compras/<int:id>', methods=['DELETE'])
def eliminar_compra(id):
    return eliminar_compra_controller(id)
