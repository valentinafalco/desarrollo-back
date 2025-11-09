import os
import logging
import base64
from datetime import datetime
from main.extension import db
from main.dominios.track.modelo_track import Track
from main.dominios.genero.modelo_genero import Genero
from main.dominios.discografica.modelo_discografica import Discografica
from main.dominios.usuario.modelo_usuario import Usuario

# Carpeta donde se guardarán los audios
UPLOAD_FOLDER = "main/static/uploads/audios"


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):
    if 'nombreTrack' not in data or not data['nombreTrack'].strip():
        raise ValueError("El campo 'nombreTrack' es obligatorio.")

    if 'fechaLanzamiento' in data and data['fechaLanzamiento']:
        try:
            datetime.strptime(data['fechaLanzamiento'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY-MM-DD.")

    if 'idGenero' in data and data['idGenero']:
        if not Genero.query.get(data['idGenero']):
            raise ValueError("El género no existe.")

    if 'idDiscografica' in data and data['idDiscografica']:
        if not Discografica.query.get(data['idDiscografica']):
            raise ValueError("La discográfica no existe.")

    if 'idUsuario' in data and data['idUsuario']:
        if not Usuario.query.get(data['idUsuario']):
            raise ValueError("El usuario no existe.")


# -------------------- CREAR TRACK --------------------

def crear_track(data, archivo_audio=None, archivo_imagen=None):
    try:
        validar_campos(data)

        # Procesar imagen (archivo o base64)
        imagen_bytes = None
        if archivo_imagen:
            if not archivo_imagen.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValueError("La imagen debe ser formato .jpg o .png")
            imagen_bytes = archivo_imagen.read()
        else:
            imagen_base64 = data.get('imagenTrack')
            imagen_bytes = base64.b64decode(imagen_base64) if imagen_base64 else None

        # Procesar archivo de audio (si se envía)
        link_audio = None
        if archivo_audio:
            if not archivo_audio.filename.endswith(".mp3"):
                raise ValueError("El archivo debe ser formato .mp3")
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            nombre_archivo = archivo_audio.filename
            ruta_archivo = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            archivo_audio.save(ruta_archivo)
            link_audio = f"/static/uploads/audios/{nombre_archivo}"

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
            reproduccionesTrack=data.get('reproduccionesTrack', 0),
            linkAudio=link_audio
        )

        db.session.add(nuevo_track)
        db.session.commit()
        return nuevo_track

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear el track")
        raise e


# -------------------- ACTUALIZAR TRACK --------------------

def actualizar_track(id, data, archivo_audio=None, archivo_imagen=None):
    track = Track.query.get(id)
    if not track:
        raise ValueError("Track no encontrado.")

    try:
        validar_campos(data)

        # Imagen nueva (archivo o base64)
        if archivo_imagen:
            if not archivo_imagen.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValueError("La imagen debe ser formato .jpg o .png")
            track.imagenTrack = archivo_imagen.read()
        else:
            imagen_base64 = data.get('imagenTrack')
            if imagen_base64:
                track.imagenTrack = base64.b64decode(imagen_base64)

        # Audio nuevo (opcional)
        if archivo_audio:
            if not archivo_audio.filename.endswith(".mp3"):
                raise ValueError("El archivo debe ser formato .mp3")
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            nombre_archivo = archivo_audio.filename
            ruta_archivo = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            archivo_audio.save(ruta_archivo)
            track.linkAudio = f"/static/uploads/audios/{nombre_archivo}"

        # Otros campos
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

# -------------------- SUMAR LIKE --------------------

def sumar_like(id):
    track = Track.query.get(id)
    if not track:
        raise ValueError("Track no encontrado.")

    try:
        track.favoritosTrack = (track.favoritosTrack or 0) + 1
        db.session.commit()
        return track
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al sumar like al track")
        raise e

# -------------------- SUMAR REPRODUCCIÓN --------------------

def sumar_reproduccion(id):
    track = Track.query.get(id)
    if not track:
        raise ValueError("Track no encontrado.")

    try:
        track.reproduccionesTrack = (track.reproduccionesTrack or 0) + 1
        db.session.commit()
        return track
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al sumar reproducción al track")
        raise e
