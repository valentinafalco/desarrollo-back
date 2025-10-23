from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.discografica.service_discografica import (
    crear_discografica,
    actualizar_discografica,
    eliminar_discografica,
    listar_discograficas,
    obtener_discografica
)


# -------------------- CREAR --------------------

def crear_discografica_controller():

    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos validos'}), 400

    try:
        discografica = crear_discografica(data)
        return jsonify(discografica.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la discografica")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear la discografica")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- MODIFICAR --------------------

def modificar_discografica_controller(id):

    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos validos'}), 400

    try:
        discografica = actualizar_discografica(id, data)
        return jsonify(discografica.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception:
        logging.exception("Error al modificar la discografica")
        return jsonify({'error': 'Error al modificar la discografica'}), 500


# -------------------- ELIMINAR --------------------

def eliminar_discografica_controller(id):

    try:
        resultado = eliminar_discografica(id)

        if not resultado:
            raise ValueError("No se pudo eliminar la discografica.")
        return jsonify({'mensaje': 'Discografica eliminada correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception:
        logging.exception("Error al eliminar la discografica")
        return jsonify({'error': 'Error al eliminar la discografica'}), 500


# -------------------- LISTAR --------------------

def listar_discograficas_controller():

    try:
        discograficas = listar_discograficas()
        return jsonify([d.serialize() for d in discograficas]), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception:
        logging.exception("Error al listar las discograficas")
        return jsonify({'error': 'Error al listar las discograficas'}), 500


# -------------------- OBTENER --------------------

def obtener_discografica_controller(id):

    try:
        discografica = obtener_discografica(id)
        return jsonify(discografica.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception:
        logging.exception("Error al obtener la discografica")
        return jsonify({'error': 'Error al obtener la discografica'}), 500

