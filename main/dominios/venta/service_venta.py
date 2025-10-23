import logging
from datetime import datetime
from main.extension import db
from main.dominios.venta.modelo_venta import Venta
from main.dominios.usuario.modelo_usuario import Usuario
from main.dominios.track.modelo_track import Track


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):

    campos_obligatorios = ['idUsuario', 'idTrack']

    # Verificar campos requeridos
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo]:
            raise ValueError(f"El campo '{campo}' no puede estar vacío")

    # Validar existencia de Usuario y Track
    if not Usuario.query.get(data['idUsuario']):
        raise ValueError("Usuario no válido o inexistente")

    if not Track.query.get(data['idTrack']):
        raise ValueError("Track no válido o inexistente")

    # Validar formato de fecha (opcional)
    if 'fechaVenta' in data and data['fechaVenta']:
        try:
            fecha = datetime.strptime(data['fechaVenta'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY-MM-DD HH:MM:SS")
    else:
        fecha = datetime.utcnow()  # Fecha actual por defecto

    return fecha


# -------------------- CREAR VENTA --------------------

def crear_venta(data):
    fecha = validar_campos(data)

    try:
        venta = Venta(
            idUsuario=data['idUsuario'],
            idTrack=data['idTrack'],
            fechaVenta=fecha
        )
        db.session.add(venta)
        db.session.commit()
        return venta
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la venta")
        raise e


# -------------------- ACTUALIZAR VENTA --------------------

def actualizar_venta(id, data):
    venta = Venta.query.get(id)
    if not venta:
        raise ValueError("Venta no encontrada")

    fecha = validar_campos(data)

    try:
        venta.idUsuario = data['idUsuario']
        venta.idTrack = data['idTrack']
        venta.fechaVenta = fecha

        db.session.commit()
        return venta
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la venta")
        raise e


# -------------------- ELIMINAR VENTA --------------------

def eliminar_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        raise ValueError("Venta no encontrada")

    try:
        db.session.delete(venta)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar la venta")
        raise e


# -------------------- LISTAR VENTAS --------------------

def listar_ventas():
    try:
        ventas = Venta.query.all()
        if not ventas:
            raise ValueError("No hay ventas registradas")
        return ventas
    except Exception as e:
        logging.exception("Error al listar las ventas")
        raise e


# -------------------- OBTENER VENTA --------------------

def obtener_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        raise ValueError("Venta no encontrada")
    return venta
