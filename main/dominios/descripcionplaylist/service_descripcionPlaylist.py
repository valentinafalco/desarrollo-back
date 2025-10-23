import logging
import base64
from main.extension import db
from main.dominios.descripcionplaylist.modelo_descripcionPlaylist import DescripcionPlaylist


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):
    campos_obligatorios = ['nombrePlaylist']

    # Verificar que esté presente el campo obligatorio
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo] or not str(data[campo]).strip():
            raise ValueError(f"El campo '{campo}' no puede estar vacío")

    # Validar longitud del nombre
    if len(data['nombrePlaylist']) > 50:
        raise ValueError("El campo 'nombrePlaylist' no puede superar los 50 caracteres")

    # Validar longitud de la descripción si existe
    if 'descripcionPlaylist' in data and data['descripcionPlaylist']:
        if len(data['descripcionPlaylist']) > 5000:
            raise ValueError("El campo 'descripcionPlaylist' no puede superar los 5000 caracteres")

    # Validar imagen (si existe y es base64 válida)
    imagen_bytes = None
    if 'imagenPlaylist' in data and data['imagenPlaylist']:
        try:
            imagen_bytes = base64.b64decode(data['imagenPlaylist'])
        except Exception:
            raise ValueError("La imagen debe estar en formato base64 válido")

    return imagen_bytes


# -------------------- CREAR DESCRIPCIÓN PLAYLIST --------------------

def crear_descripcion_playlist(data):
    imagen_bytes = validar_campos(data)

    try:
        descripcion = DescripcionPlaylist(
            nombrePlaylist=data['nombrePlaylist'].strip(),
            imagenPlaylist=imagen_bytes,
            descripcionPlaylist=data.get('descripcionPlaylist', '').strip() or None
        )
        db.session.add(descripcion)
        db.session.commit()
        return descripcion
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la descripción de playlist")
        raise e


# -------------------- ACTUALIZAR DESCRIPCIÓN PLAYLIST --------------------

def actualizar_descripcion_playlist(id, data):
    descripcion = DescripcionPlaylist.query.get(id)
    if not descripcion:
        raise ValueError("Descripción de playlist no encontrada")

    imagen_bytes = validar_campos(data)

    try:
        descripcion.nombrePlaylist = data['nombrePlaylist'].strip()
        descripcion.imagenPlaylist = imagen_bytes
        descripcion.descripcionPlaylist = data.get('descripcionPlaylist', '').strip() or None

        db.session.commit()
        return descripcion
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la descripción de playlist")
        raise e


# -------------------- ELIMINAR DESCRIPCIÓN PLAYLIST --------------------

def eliminar_descripcion_playlist(id):
    descripcion = DescripcionPlaylist.query.get(id)
    if not descripcion:
        raise ValueError("Descripción de playlist no encontrada")

    try:
        db.session.delete(descripcion)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar la descripción de playlist")
        raise e


# -------------------- LISTAR DESCRIPCIONES --------------------

def listar_descripciones_playlist():
    try:
        descripciones = DescripcionPlaylist.query.all()
        if not descripciones:
            raise ValueError("No hay descripciones de playlist registradas")
        return descripciones
    except Exception as e:
        logging.exception("Error al listar las descripciones de playlist")
        raise e


# -------------------- OBTENER DESCRIPCIÓN --------------------

def obtener_descripcion_playlist(id):
    descripcion = DescripcionPlaylist.query.get(id)
    if not descripcion:
        raise ValueError("Descripción de playlist no encontrada")
    return descripcion
