from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.playlist.service_playlist import (
    crear_playlist,
    actualizar_playlist,
    eliminar_playlist,
    listar_playlists,
    obtener_playlist
)


# -------------------- CREAR PLAYLIST --------------------
def crear_playlist_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        playlist = crear_playlist(data)
        if not playlist:
            raise ValueError("Error al crear la playlist.")
        return jsonify(playlist.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear la playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR PLAYLIST --------------------
def modificar_playlist_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        playlist = actualizar_playlist(id, data)
        return jsonify(playlist.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar la playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al modificar la playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR PLAYLIST --------------------
def eliminar_playlist_controller(id):
    try:
        resultado = eliminar_playlist(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la playlist.")
        return jsonify({'mensaje': 'Playlist eliminada correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar la playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al eliminar la playlist")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR PLAYLISTS --------------------
def listar_playlists_controller():
    try:
        playlists = listar_playlists()
        playlists_serializadas = [p.serialize() for p in playlists]
        return jsonify(playlists_serializadas), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar las playlists")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al listar las playlists")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER PLAYLIST --------------------
def obtener_playlist_controller(id):
    try:
        playlist = obtener_playlist(id)
        return jsonify(playlist.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener la playlist")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al obtener la playlist")
        return jsonify({'error': 'Error en el servidor'}), 500