from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.ubicacion.service_ubicacion import (
    crear_ubicacion,
    actualizar_ubicacion,
    eliminar_ubicacion,
    listar_ubicaciones,
    obtener_ubicacion
)

# -------------------- CREAR UBICACIÓN --------------------
def crear_ubicacion_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        ubicacion = crear_ubicacion(data)
        if not ubicacion:
            raise ValueError("Error al crear la ubicación.")
        return jsonify(ubicacion.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la ubicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear la ubicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR UBICACIÓN --------------------
def modificar_ubicacion_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        ubicacion = actualizar_ubicacion(id, data)
        return jsonify(ubicacion.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar la ubicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar la ubicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR UBICACIÓN --------------------
def eliminar_ubicacion_controller(id):
    try:
        resultado = eliminar_ubicacion(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la ubicación.")
        return jsonify({'mensaje': 'Ubicación eliminada correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar la ubicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar la ubicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR UBICACIONES --------------------
def listar_ubicaciones_controller():
    try:
        ubicaciones = listar_ubicaciones()
        ubicaciones_serializadas = [u.serialize() for u in ubicaciones]
        return jsonify(ubicaciones_serializadas), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar las ubicaciones")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar las ubicaciones")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER UBICACIÓN --------------------
def obtener_ubicacion_controller(id):
    try:
        ubicacion = obtener_ubicacion(id)
        return jsonify(ubicacion.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener la ubicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener la ubicación")
        return jsonify({'error': 'Error en el servidor'}), 500