from flask import Blueprint, request
from main.dominios.genero.controller_genero import (
	listar_generos_controller,
	obtener_genero_controller,
	crear_genero_controller,
	modificar_genero_controller,
	eliminar_genero_controller
)

# Crear blueprint para agrupar rutas relacionadas con Genero

genero_bp = Blueprint('genero', __name__)

# GET - Listar todos los generos
@genero_bp.route('/generos', methods=['GET'])
def listar_generos():
	return listar_generos_controller()

# GET - Obtener un genero por ID
@genero_bp.route('/generos/<int:id>', methods=['GET'])
def obtener_genero(id):
	return obtener_genero_controller(id)

# POST - Crear un nuevo genero
@genero_bp.route('/generos', methods=['POST'])
def crear_genero():
	return crear_genero_controller()

# PUT - Modificar un genero existente
@genero_bp.route('/generos/<int:id>', methods=['PUT'])
def modificar_genero(id):
	return modificar_genero_controller(id)

# DELETE - Eliminar un genero
@genero_bp.route('/generos/<int:id>', methods=['DELETE'])
def eliminar_genero(id):
	return eliminar_genero_controller(id)


