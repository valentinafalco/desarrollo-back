from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.metodoPago.service_metodoPago import (
    crear_metodo_pago,
    actualizar_metodo_pago,
    eliminar_metodo_pago,
    listar_metodos_pago,
    obtener_metodo_pago
)


# -------------------- CREAR MÉTODO DE PAGO --------------------
def crear_metodo_pago_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        metodo = crear_metodo_pago(data)
        if not metodo:
            raise ValueError("Error al crear el método de pago.")
        return jsonify(metodo.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear el método de pago")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear el método de pago")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR MÉTODO DE PAGO --------------------
def modificar_metodo_pago_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        metodo = actualizar_metodo_pago(id, data)
        return jsonify(metodo.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar el método de pago")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar el método de pago")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR MÉTODO DE PAGO --------------------
def eliminar_metodo_pago_controller(id):
    try:
        resultado = eliminar_metodo_pago(id)
        if not resultado:
            raise ValueError("No se pudo eliminar el método de pago.")
        return jsonify({'mensaje': 'Método de pago eliminado correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar el método de pago")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar el método de pago")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR MÉTODOS DE PAGO --------------------
def listar_metodos_pago_controller():
    try:
        metodos = listar_metodos_pago()
        metodos_serializados = [m.serialize() for m in metodos]
        return jsonify(metodos_serializados), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar los métodos de pago")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar los métodos de pago")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER MÉTODO DE PAGO --------------------
def obtener_metodo_pago_controller(id):
    try:
        metodo = obtener_metodo_pago(id)
        return jsonify(metodo.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener el método de pago")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener el método de pago")
        return jsonify({'error': 'Error en el servidor'}), 500