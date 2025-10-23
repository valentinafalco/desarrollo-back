import logging
from main.extension import db
from main.dominios.playlist.modelo_playlist import Playlist
from main.dominios.usuario.modelo_usuario import Usuario
from main.dominios.descripcionplaylist.modelo_descripcionPlaylist import DescripcionPlaylist
from main.dominios.track.modelo_track import Track


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):
    campos_obligatorios = ['idUsuario', 'idDescripcionPlaylist', 'idTrack']

    # Verificar presencia y contenido
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo]:
            raise ValueError(f"El campo '{campo}' no puede estar vacío")

    # Validar existencia de claves foráneas
    if not Usuario.query.get(data['idUsuario']):
        raise ValueError("Usuario no válido o inexistente")

    if not DescripcionPlaylist.query.get(data['idDescripcionPlaylist']):
        raise ValueError("Descripción de playlist no válida o inexistente")

    if not Track.query.get(data['idTrack']):
        raise ValueError("Track no válido o inexistente")

    return True


# -------------------- CREAR PLAYLIST --------------------

def crear_playlist(data):
    validar_campos(data)

    try:
        playlist = Playlist(
            idUsuario=data['idUsuario'],
            idDescripcionPlaylist=data['idDescripcionPlaylist'],
            idTrack=data['idTrack']
        )
        db.session.add(playlist)
        db.session.commit()
        return playlist
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la playlist")
        raise e


# -------------------- ACTUALIZAR PLAYLIST --------------------

def actualizar_playlist(id, data):
    playlist = Playlist.query.get(id)
    if not playlist:
        raise ValueError("Playlist no encontrada")

    validar_campos(data)

    try:
        playlist.idUsuario = data['idUsuario']
        playlist.idDescripcionPlaylist = data['idDescripcionPlaylist']
        playlist.idTrack = data['idTrack']

        db.session.commit()
        return playlist
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la playlist")
        raise e


# -------------------- ELIMINAR PLAYLIST --------------------

def eliminar_playlist(id):
    playlist = Playlist.query.get(id)
    if not playlist:
        raise ValueError("Playlist no encontrada")

    try:
        db.session.delete(playlist)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar la playlist")
        raise e


# -------------------- LISTAR PLAYLISTS --------------------

def listar_playlists():
    try:
        playlists = Playlist.query.all()
        if not playlists:
            raise ValueError("No hay playlists registradas")
        return playlists
    except Exception as e:
        logging.exception("Error al listar las playlists")
        raise e


# -------------------- OBTENER PLAYLIST --------------------

def obtener_playlist(id):
    playlist = Playlist.query.get(id)
    if not playlist:
        raise ValueError("Playlist no encontrada")
    return playlist
