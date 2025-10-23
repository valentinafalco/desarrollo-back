from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.descripcionplaylist.service_descripcionPlaylist import (
    crear_descripcion_playlist,
    actualizar_descripcion_playlist,
    eliminar_descripcion_playlist,
    listar_descripciones_playlist,
    obtener_descripcion_playlist
)


# -------------------- CREAR DESCRIPCIÓN PLAYLIST --------------------
def crear_descripcion_playlist_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        descripcion = crear_descripcion_playlist(data)
        if not descripcion:
            raise ValueError("Error al crear la descripción de playlist.")
        return jsonify(descripcion.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la descripción de playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear la descripción de playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR DESCRIPCIÓN PLAYLIST --------------------
def modificar_descripcion_playlist_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        descripcion = actualizar_descripcion_playlist(id, data)
        return jsonify(descripcion.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar la descripción de playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar la descripción de playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR DESCRIPCIÓN PLAYLIST --------------------
def eliminar_descripcion_playlist_controller(id):
    try:
        resultado = eliminar_descripcion_playlist(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la descripción de playlist.")
        return jsonify({'mensaje': 'Descripción de playlist eliminada correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar la descripción de playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar la descripción de playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR DESCRIPCIONES PLAYLIST --------------------
def listar_descripciones_playlist_controller():
    try:
        descripciones = listar_descripciones_playlist()
        descripciones_serializadas = [d.serialize() for d in descripciones]
        return jsonify(descripciones_serializadas), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar las descripciones de playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar las descripciones de playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER DESCRIPCIÓN PLAYLIST --------------------
def obtener_descripcion_playlist_controller(id):
    try:
        descripcion = obtener_descripcion_playlist(id)
        return jsonify(descripcion.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener la descripción de playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener la descripción de playlist")
        return jsonify({'error': 'Error en el servidor'}), 500