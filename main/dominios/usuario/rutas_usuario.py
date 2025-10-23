from flask import Blueprint, request
from main.dominios.usuario.controller_usuario import (
    listar_usuarios_controller,
    obtener_usuario_controller,
    crear_usuario_controller,
    actualizar_usuario_controller,
    eliminar_usuario_controller
)

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return listar_usuarios_controller()

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    return obtener_usuario_controller(id)

@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    return crear_usuario_controller()

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    return actualizar_usuario_controller(id)

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    return eliminar_usuario_controller(id)
