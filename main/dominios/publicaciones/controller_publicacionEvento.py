from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.publicaciones.service_publicacionEvento import (
    crear_publicacion_evento,
    actualizar_publicacion_evento,
    eliminar_publicacion_evento,
    listar_publicaciones_evento,
    obtener_publicacion_evento
)


# -------------------- CREAR --------------------
def crear_publicacion_evento_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        publicacion = crear_publicacion_evento(data)
        return jsonify(publicacion.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la publicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear la publicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR --------------------
def modificar_publicacion_evento_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        publicacion = actualizar_publicacion_evento(id, data)
        return jsonify(publicacion.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar la publicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar la publicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR --------------------
def eliminar_publicacion_evento_controller(id):
    try:
        ok = eliminar_publicacion_evento(id)
        if not ok:
            raise ValueError("No se pudo eliminar la publicación")
        return jsonify({'mensaje': 'Publicación eliminada correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar la publicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar la publicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR --------------------
def listar_publicaciones_evento_controller():
    try:
        publicaciones = listar_publicaciones_evento()
        return jsonify([p.serialize() for p in publicaciones]), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar publicaciones")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar publicaciones")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER POR ID --------------------
def obtener_publicacion_evento_controller(id):
    try:
        p = obtener_publicacion_evento(id)
        return jsonify(p.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener publicación")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener publicación")
        return jsonify({'error': 'Error en el servidor'}), 500
