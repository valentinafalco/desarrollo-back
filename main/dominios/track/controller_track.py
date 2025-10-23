from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.track.service_track import (
    crear_track,
    actualizar_track,
    eliminar_track,
    listar_tracks,
    obtener_track
)

# -------------------- CREAR --------------------

def crear_track_controller():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos validos'}), 400

    try:
        track = crear_track(data)
        return jsonify(track.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear el track")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception:
        logging.exception("Error inesperado al crear el track")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- MODIFICAR --------------------

def modificar_track_controller(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos validos'}), 400

    try:
        track = actualizar_track(id, data)
        return jsonify(track.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception:
        logging.exception("Error al modificar el track")
        return jsonify({'error': 'Error al modificar el track'}), 500


# -------------------- ELIMINAR --------------------

def eliminar_track_controller(id):

    try:
        resultado = eliminar_track(id)

        if not resultado:
            raise ValueError("No se pudo eliminar el track.")
        return jsonify({'mensaje': 'Track eliminado correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception:
        logging.exception("Error al eliminar el track")
        return jsonify({'error': 'Error al eliminar el track'}), 500


# -------------------- LISTAR --------------------

def listar_tracks_controller():

    try:
        tracks = listar_tracks()
        return jsonify([t.serialize() for t in tracks]), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception:
        logging.exception("Error al listar los tracks")
        return jsonify({'error': 'Error al listar los tracks'}), 500


# -------------------- OBTENER --------------------

def obtener_track_controller(id):

    try:
        track = obtener_track(id)
        return jsonify(track.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception:
        logging.exception("Error al obtener el track")
        return jsonify({'error': 'Error al obtener el track'}), 500

