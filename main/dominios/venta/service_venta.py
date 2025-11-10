import logging
from datetime import datetime

from sqlalchemy.orm import joinedload
from main.extension import db

from main.dominios.venta.modelo_venta import Venta
from main.dominios.usuario.modelo_usuario import Usuario
from main.dominios.track.modelo_track import Track
from main.dominios.compra.modelo_compra import Compra  # 👈 usamos compras para derivar ventas


# -------------------- VALIDAR CAMPOS (para endpoints CRUD de Venta) --------------------

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


# -------------------- CREAR / ACTUALIZAR / ELIMINAR (para tabla Venta real) --------------------

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


# -------------------- LISTAR / OBTENER  --------------------
# 🔹 Clave: Listamos VENTAS derivadas de COMPRAS (Compra JOIN Track),
#     filtrando por vendedor (dueño del track) si se pasa id_usuario_vendedor.

def listar_ventas(id_usuario_vendedor: int | None = None):
    """
    Devuelve 'ventas' derivadas de la tabla Compra, filtrando por el dueño del track (vendedor).
    Si id_usuario_vendedor es None, devuelve TODAS las ventas del sistema (todas las compras).

    Retorna: lista de objetos Compra con .track cargado (usuario/discografica/genero).
    """
    try:
        q = (
            db.session.query(Compra)
            .join(Track, Compra.idTrack == Track.idTrack)
            .options(
                joinedload(Compra.track).joinedload(Track.usuario),       # nombreUsuario del dueño
                joinedload(Compra.track).joinedload(Track.discografica),  # opcional
                joinedload(Compra.track).joinedload(Track.genero),        # opcional
            )
        )
        if id_usuario_vendedor is not None:
            q = q.filter(Track.idUsuario == id_usuario_vendedor)

        return q.all()
    except Exception as e:
        logging.exception("Error al listar las ventas derivadas de compras")
        raise e


def obtener_venta(id):
    """
    Si necesitás seguir usando la tabla Venta real para obtener por id, se deja igual.
    Para 'ventas derivadas', lo normal es no usar este get puntual.
    """
    venta = Venta.query.get(id)
    if not venta:
        raise ValueError("Venta no encontrada")
    return venta
