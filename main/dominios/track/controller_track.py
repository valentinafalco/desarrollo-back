from flask import request, jsonify
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.track.service_track import (
    crear_track,
    actualizar_track,
    eliminar_track,
    listar_tracks,
    obtener_track,
    sumar_like,
    sumar_reproduccion
)

# -------------------- CREAR TRACK --------------------

def crear_track_controller():
    try:
        # Recibe datos (form-data)
        data = request.form.to_dict()
        archivo_audio = request.files.get('audio')   # campo del mp3
        archivo_imagen = request.files.get('imagen') # campo de la imagen

        print("FORM DATA:", data)
        print("AUDIO:", archivo_audio)
        print("IMAGEN:", archivo_imagen)

        if not data and not archivo_audio and not archivo_imagen:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400

        track = crear_track(data, archivo_audio, archivo_imagen)
        return jsonify(track.serialize()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear el track")
        return jsonify({'error': 'Error en la base de datos'}), 500

    except Exception as e:
        logging.exception("Error inesperado al crear el track")
        return jsonify({'error': str(e)}), 500


# -------------------- MODIFICAR TRACK --------------------

def modificar_track_controller(id):
    try:
        data = request.form.to_dict()
        archivo_audio = request.files.get('audio')
        archivo_imagen = request.files.get('imagen')

        print("🛠️ MODIFICAR DATA:", data)
        print("🎵 AUDIO:", archivo_audio)
        print("🖼️ IMAGEN:", archivo_imagen)

        if not data and not archivo_audio and not archivo_imagen:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400

        track = actualizar_track(id, data, archivo_audio, archivo_imagen)
        return jsonify(track.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        logging.exception("Error al modificar el track")
        return jsonify({'error': str(e)}), 500


# -------------------- ELIMINAR TRACK --------------------

def eliminar_track_controller(id):
    try:
        resultado = eliminar_track(id)
        if not resultado:
            raise ValueError("No se pudo eliminar el track.")
        return jsonify({'mensaje': 'Track eliminado correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception as e:
        logging.exception("Error al eliminar el track")
        return jsonify({'error': str(e)}), 500


# -------------------- LISTAR TRACKS --------------------

def listar_tracks_controller():
    try:
        tracks = listar_tracks()
        return jsonify([t.serialize() for t in tracks]), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception as e:
        logging.exception("Error al listar los tracks")
        return jsonify({'error': str(e)}), 500


# -------------------- OBTENER TRACK --------------------

def obtener_track_controller(id):
    try:
        track = obtener_track(id)
        return jsonify(track.serialize()), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404

    except Exception as e:
        logging.exception("Error al obtener el track")
        return jsonify({'error': str(e)}), 500

# -------------------- SUMAR LIKE --------------------

def sumar_like_controller(id):
    try:
        track = sumar_like(id)
        return jsonify({
            'mensaje': 'Like agregado correctamente',
            'idTrack': track.idTrack,
            'favoritosTrack': track.favoritosTrack
        }), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al sumar like")
        return jsonify({'error': str(e)}), 500

# -------------------- SUMAR REPRODUCCIÓN --------------------

def sumar_reproduccion_controller(id):
    try:
        track = sumar_reproduccion(id)
        return jsonify({
            'mensaje': 'Reproducción registrada correctamente',
            'idTrack': track.idTrack,
            'reproduccionesTrack': track.reproduccionesTrack
        }), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al sumar reproducción")
        return jsonify({'error': str(e)}), 500
