from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.evento.service_evento import (
    crear_evento,
    actualizar_evento,
    eliminar_evento,
    listar_eventos,
    obtener_evento
)

# -------------------- CREAR EVENTO --------------------
def crear_evento_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        evento = crear_evento(data)
        if not evento:
            raise ValueError("Error al crear el evento.")
        return jsonify(evento.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear el evento")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear el evento")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR EVENTO --------------------
def modificar_evento_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        evento = actualizar_evento(id, data)
        return jsonify(evento.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar el evento")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar el evento")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR EVENTO --------------------
def eliminar_evento_controller(id):
    try:
        resultado = eliminar_evento(id)
        if not resultado:
            raise ValueError("No se pudo eliminar el evento.")
        return jsonify({'mensaje': 'Evento eliminado correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar el evento")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar el evento")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR EVENTOS --------------------
def listar_eventos_controller():
    try:
        eventos = listar_eventos()
        eventos_serializados = [evento.serialize() for evento in eventos]
        return jsonify(eventos_serializados), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar los eventos")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar los eventos")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER EVENTO --------------------
def obtener_evento_controller(id):
    try:
        evento = obtener_evento(id)
        return jsonify(evento.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener el evento")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener el evento")
        return jsonify({'error': 'Error en el servidor'}), 500