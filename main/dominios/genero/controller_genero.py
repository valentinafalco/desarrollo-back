from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.genero.service_genero import (
    crear_genero,
    actualizar_genero,
    eliminar_genero,
    listar_generos,
    obtener_genero
)

# ---------------- CREAR GÉNERO ----------------
def crear_genero_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        genero = crear_genero(data)
        return jsonify(genero.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError as e:
        logging.exception("Error en la base de datos al crear el género")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception as e:
        logging.exception("Error inesperado al crear el género")
        return jsonify({'error': 'Error en el servidor'}), 500


# ---------------- ACTUALIZAR GÉNERO ----------------
def modificar_genero_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        genero = actualizar_genero(id, data)
        return jsonify(genero.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        logging.exception("Error al modificar el género")
        return jsonify({'error': 'Error al modificar el género'}), 500


# ---------------- ELIMINAR GÉNERO ----------------
def eliminar_genero_controller(id):
    try:
        resultado = eliminar_genero(id)
        if not resultado:
            raise ValueError("No se pudo eliminar el género.")
        return jsonify({'mensaje': 'Género eliminado correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        logging.exception("Error al eliminar el género")
        return jsonify({'error': 'Error al eliminar el género'}), 500


# ---------------- LISTAR GÉNEROS ----------------
def listar_generos_controller():
    try:
        generos = listar_generos()
        generos_serializados = [g.serialize() for g in generos]
        return jsonify(generos_serializados), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception as e:
        logging.exception("Error al listar los géneros")
        return jsonify({'error': 'Error al listar los géneros'}), 500


# ---------------- OBTENER GÉNERO ----------------
def obtener_genero_controller(id):
    try:
        genero = obtener_genero(id)
        return jsonify(genero.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception as e:
        logging.exception("Error al obtener el género")
        return jsonify({'error': 'Error al obtener el género'}), 500
