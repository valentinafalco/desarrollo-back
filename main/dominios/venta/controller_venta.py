from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.venta.service_venta import (
    crear_venta,
    actualizar_venta,
    eliminar_venta,
    listar_ventas,
    obtener_venta
)


# -------------------- CREAR VENTA --------------------
def crear_venta_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        venta = crear_venta(data)
        if not venta:
            raise ValueError("Error al crear la venta.")
        return jsonify(venta.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear la venta")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR VENTA --------------------
def modificar_venta_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        venta = actualizar_venta(id, data)
        return jsonify(venta.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar la venta")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR VENTA --------------------
def eliminar_venta_controller(id):
    try:
        resultado = eliminar_venta(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la venta.")
        return jsonify({'mensaje': 'Venta eliminada correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar la venta")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR VENTAS --------------------
def listar_ventas_controller():
    try:
        ventas = listar_ventas()
        ventas_serializadas = [v.serialize() for v in ventas]
        return jsonify(ventas_serializadas), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar las ventas")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar las ventas")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER VENTA --------------------
def obtener_venta_controller(id):
    try:
        venta = obtener_venta(id)
        return jsonify(venta.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener la venta")
        return jsonify({'error': 'Error en el servidor'}), 500