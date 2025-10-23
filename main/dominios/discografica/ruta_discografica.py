from flask import Blueprint
from main.dominios.discografica.controller_discografica import (
    listar_discograficas_controller,
    obtener_discografica_controller,
    crear_discografica_controller,
    modificar_discografica_controller,
    eliminar_discografica_controller
)

# Crear blueprint para agrupar rutas relacionadas con Discografica

discografica_bp = Blueprint('discografica', __name__)

# GET - Listar todas las Discograficas
@discografica_bp.route('/discograficas', methods=['GET'])
def listar_discograficas():
    return listar_discograficas_controller()

# GET - Obtener una discografica por ID
@discografica_bp.route('/discograficas/<int:id>', methods=['GET'])
def obtener_discografica(id):
    return obtener_discografica_controller(id)

# POST - Crear una nueva discografica
@discografica_bp.route('/discograficas', methods=['POST'])
def crear_discografica():
    return crear_discografica_controller()

# PUT - Modificar una discografica existente
@discografica_bp.route('/discograficas/<int:id>', methods=['PUT'])
def modificar_discografica(id):
    return modificar_discografica_controller(id)

# DELETE - Eliminar una discografica
@discografica_bp.route('/discograficas/<int:id>', methods=['DELETE'])
def eliminar_discografica(id):
    return eliminar_discografica_controller(id)

