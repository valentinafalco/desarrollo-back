from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.compra.service_compra import (
    crear_compra,
    actualizar_compra,
    eliminar_compra,
    obtener_compra,
    listar_compras
)

# -------------------- CREAR COMPRA --------------------
def crear_compra_controller(data):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        compra = crear_compra(data)
        if not compra:
            raise ValueError("Error al crear la compra.")
        return jsonify(compra.serialize()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        logging.exception("Error en la base de datos al crear la compra")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception as e:
        logging.exception("Error inesperado al crear la compra")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR COMPRA --------------------
def modificar_compra_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        compra = actualizar_compra(id, data)
        return jsonify(compra.serialize()), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.exception("Error al modificar la compra")
        return jsonify({'error': f'Error al modificar la compra: {str(e)}'}), 500


# -------------------- ELIMINAR COMPRA --------------------
def eliminar_compra_controller(id):
    try:
        resultado = eliminar_compra(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la compra.")
        return jsonify({'mensaje': 'Compra eliminada correctamente'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al eliminar la compra")
        return jsonify({'error': f'Error al eliminar la compra: {str(e)}'}), 500


# -------------------- LISTAR COMPRAS --------------------
def listar_compras_controller():
    try:
        compras = listar_compras()
        compras_serializadas = [compra.serialize() for compra in compras]
        return jsonify(compras_serializadas), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al listar las compras")
        return jsonify({'error': f'Error al listar las compras: {str(e)}'}), 500


# -------------------- OBTENER COMPRA --------------------
def obtener_compra_controller(id):
    try:
        compra = obtener_compra(id)
        return jsonify(compra.serialize()), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al obtener la compra")
        return jsonify({'error': f'Error al obtener la compra: {str(e)}'}), 500
