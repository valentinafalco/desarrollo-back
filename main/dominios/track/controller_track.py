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

# -------- Helper: serialización pública enriquecida --------
def _serialize_track_public(t):
    """
    Enriquecer el serialize del Track con datos de usuario.
    - Incluye usuario: { idUsuario, nombreUsuario }
    - Rellena 'artista' con nombreUsuario si existe.
    - Mantiene compatibilidad con t.serialize() original.
    """
    # Base del modelo
    base = {}
    try:
        base = t.serialize()
    except Exception:
        # fallback muy básico si el modelo no tiene serialize
        base = {
            "idTrack": getattr(t, "idTrack", None) or getattr(t, "id", None),
            "nombreTrack": getattr(t, "nombreTrack", None) or getattr(t, "titulo", None),
            "precio": getattr(t, "precio", None),
            "formato": getattr(t, "formato", None),
        }

    # Usuario (dueño del track)
    usuario = getattr(t, "usuario", None)
    id_usuario = None
    nombre_usuario = None
    if usuario is not None:
        id_usuario = getattr(usuario, "idUsuario", None) or getattr(usuario, "id", None)
        nombre_usuario = getattr(usuario, "nombreUsuario", None) or getattr(usuario, "nombre", None)

    # También intentar leer idUsuario directo del track por si existe FK plana
    id_usuario = id_usuario or getattr(t, "idUsuario", None)

    # Armar objeto usuario en la respuesta
    base["usuario"] = {
        "idUsuario": id_usuario,
        "nombreUsuario": nombre_usuario
    }

    # Campo plano 'artista' para el front (si no estaba)
    if not base.get("artista"):
        base["artista"] = nombre_usuario

    return base

# -------------------- CREAR TRACK --------------------
def crear_track_controller():
    try:
        data = request.form.to_dict()
        archivo_audio = request.files.get('audio')
        archivo_imagen = request.files.get('imagen')

        if not data and not archivo_audio and not archivo_imagen:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400

        track = crear_track(data, archivo_audio, archivo_imagen)
        return jsonify(_serialize_track_public(track)), 201

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

        if not data and not archivo_audio and not archivo_imagen:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400

        track = actualizar_track(id, data, archivo_audio, archivo_imagen)
        return jsonify(_serialize_track_public(track)), 200

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
        return jsonify([_serialize_track_public(t) for t in tracks]), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al listar los tracks")
        return jsonify({'error': str(e)}), 500

# -------------------- OBTENER TRACK --------------------
def obtener_track_controller(id):
    try:
        track = obtener_track(id)
        return jsonify(_serialize_track_public(track)), 200
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
