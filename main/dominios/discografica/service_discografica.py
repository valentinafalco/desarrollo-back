from main.extension import db
from main.dominios.discografica.modelo_discografica import Discografica
import logging
import base64


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):
    if 'nombreDiscografica' not in data or not data['nombreDiscografica'].strip():
        raise ValueError("El campo 'nombreDiscografica' es obligatorio.")
    return data['nombreDiscografica'].strip()


# -------------------- CREAR DISCOGRÁFICA --------------------

def crear_discografica(data):
    try:
        nombre = validar_campos(data)
        descripcion = data.get('descripcionDiscografica')

        # Procesar imagen si se envía en base64
        imagen_base64 = data.get('imagenDiscografica')
        imagen_bytes = base64.b64decode(imagen_base64) if imagen_base64 else None

        nueva = Discografica(
            nombreDiscografica=nombre,
            descripcionDiscografica=descripcion,
            imagenDiscografica=imagen_bytes
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la discográfica")
        raise e


# -------------------- ACTUALIZAR DISCOGRAFICA --------------------

def actualizar_discografica(id, data):
    discografica = Discografica.query.get(id)
    if not discografica:
        raise ValueError("Discográfica no encontrada.")

    try:
        nombre = validar_campos(data)
        descripcion = data.get('descripcionDiscografica')
        imagen_base64 = data.get('imagenDiscografica')

        discografica.nombreDiscografica = nombre
        discografica.descripcionDiscografica = descripcion

        # Si se envía una nueva imagen, la reemplaza
        if imagen_base64:
            discografica.imagenDiscografica = base64.b64decode(imagen_base64)

        db.session.commit()
        return discografica

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la discográfica")
        raise e


# -------------------- ELIMINAR DISCOGRAFICA --------------------

def eliminar_discografica(id):
    discografica = Discografica.query.get(id)
    if not discografica:
        raise ValueError("Discográfica no encontrada.")

    try:
        db.session.delete(discografica)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar la discográfica")
        raise e


# -------------------- LISTAR DISCOGRAFICAS --------------------

def listar_discograficas():
    try:
        discograficas = Discografica.query.all()
        if not discograficas:
            raise ValueError("No hay discográficas registradas.")
        return discograficas

    except Exception as e:
        logging.exception("Error al listar las discográficas")
        raise e


# -------------------- OBTENER DISCOGRAFICA --------------------

def obtener_discografica(id):
    discografica = Discografica.query.get(id)
    if not discografica:
        raise ValueError("Discográfica no encontrada.")
    return discografica
