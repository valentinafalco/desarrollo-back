from main.extension import db
from main.dominios.track.modelo_track import Track
from main.dominios.genero.modelo_genero import Genero
from main.dominios.discografica.modelo_discografica import Discografica
from main.dominios.usuario.modelo_usuario import Usuario
import logging
import base64
from datetime import datetime

# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):

    if 'nombreTrack' not in data or not data['nombreTrack'].strip():
        raise ValueError("El campo 'nombreTrack' es obligatorio.")

    # Validar formato de fecha (opcional)

    if 'fechaLanzamiento' in data and data['fechaLanzamiento']:
        try:
            datetime.strptime(data['fechaLanzamiento'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY-MM-DD.")

    # Validar relaciones (si se envían)

    if 'idGenero' in data and data['idGenero']:
        if not Genero.query.get(data['idGenero']):
            raise ValueError("El genero no existe.")

    if 'idDiscografica' in data and data['idDiscografica']:
        if not Discografica.query.get(data['idDiscografica']):
            raise ValueError("La discografica no existe.")

    if 'idUsuario' in data and data['idUsuario']:
        if not Usuario.query.get(data['idUsuario']):
            raise ValueError("El usuario no existe.")


# -------------------- CREAR TRACK --------------------

def crear_track(data):

    try:
        validar_campos(data)

        imagen_base64 = data.get('imagenTrack')
        imagen_bytes = base64.b64decode(imagen_base64) if imagen_base64 else None

        nuevo_track = Track(
            nombreTrack=data['nombreTrack'].strip(),
            bpm=data.get('bpm'),
            duracion=data.get('duracion'),
            formatoTrack=data.get('formatoTrack'),
            precioTrack=data.get('precioTrack'),
            fechaLanzamiento=data.get('fechaLanzamiento'),
            imagenTrack=imagen_bytes,
            idDiscografica=data.get('idDiscografica'),
            idGenero=data.get('idGenero'),
            idUsuario=data.get('idUsuario'),
            favoritosTrack=data.get('favoritosTrack', 0),
            reproduccionesTrack=data.get('reproduccionesTrack', 0)
        )

        db.session.add(nuevo_track)
        db.session.commit()
        return nuevo_track

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear el track")
        raise e


# -------------------- ACTUALIZAR TRACK --------------------

def actualizar_track(id, data):
    track = Track.query.get(id)

    if not track:
        raise ValueError("Track no encontrado.")

    try:
        validar_campos(data)
        imagen_base64 = data.get('imagenTrack')

        if imagen_base64:
            track.imagenTrack = base64.b64decode(imagen_base64)

        track.nombreTrack = data.get('nombreTrack', track.nombreTrack)
        track.bpm = data.get('bpm', track.bpm)
        track.duracion = data.get('duracion', track.duracion)
        track.formatoTrack = data.get('formatoTrack', track.formatoTrack)
        track.precioTrack = data.get('precioTrack', track.precioTrack)
        track.fechaLanzamiento = data.get('fechaLanzamiento', track.fechaLanzamiento)
        track.idDiscografica = data.get('idDiscografica', track.idDiscografica)
        track.idGenero = data.get('idGenero', track.idGenero)
        track.idUsuario = data.get('idUsuario', track.idUsuario)
        track.favoritosTrack = data.get('favoritosTrack', track.favoritosTrack)
        track.reproduccionesTrack = data.get('reproduccionesTrack', track.reproduccionesTrack)

        db.session.commit()
        return track

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar el track")
        raise e


# -------------------- ELIMINAR TRACK --------------------

def eliminar_track(id):
    track = Track.query.get(id)

    if not track:
        raise ValueError("Track no encontrado.")

    try:
        db.session.delete(track)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar el track")
        raise e


# -------------------- LISTAR TRACKS --------------------

def listar_tracks():

    try:
        tracks = Track.query.all()

        if not tracks:
            raise ValueError("No hay tracks registrados.")
        return tracks

    except Exception as e:
        logging.exception("Error al listar los tracks")
        raise e


# -------------------- OBTENER TRACK --------------------

def obtener_track(id):
    track = Track.query.get(id)

    if not track:
        raise ValueError("Track no encontrado.")
    return track
