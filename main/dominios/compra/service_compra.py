import logging
from datetime import datetime
from sqlalchemy.orm import joinedload
from main.extension import db
from main.dominios.compra.modelo_compra import Compra
from main.dominios.usuario.modelo_usuario import Usuario
from main.dominios.track.modelo_track import Track
from main.dominios.metodoPago.modelo_metodoPago import MetodoPago_Usuario

# -------------------- VALIDACIONES --------------------

def validar_campos(data):
    campos_obligatorios = ['idUsuario', 'idTrack', 'idMetodo', 'fechaCompra', 'montoCompra']

    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo]:
            raise ValueError(f"El campo {campo} no puede estar vacío")

    # Validar formato de fecha
    try:
        fecha = datetime.strptime(data['fechaCompra'], '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("El formato de fecha debe ser YYYY-MM-DD")

    # Validar monto numérico
    if not isinstance(data['montoCompra'], (int, float)):
        raise ValueError("El montoCompra debe ser numérico")

    # Validar FKs
    if not Usuario.query.get(data['idUsuario']):
        raise ValueError("Usuario no válido")

    if not Track.query.get(data['idTrack']):
        raise ValueError("Track no válido")

    if not MetodoPago_Usuario.query.get(data['idMetodo']):
        raise ValueError("Método de pago no válido")

    return fecha

# -------------------- CRUD --------------------

def crear_compra(data):
    fecha = validar_campos(data)
    try:
        compra = Compra(
            idUsuario=data['idUsuario'],
            idTrack=data['idTrack'],
            idMetodo=data['idMetodo'],
            fechaCompra=fecha,
            montoCompra=data['montoCompra']
        )
        db.session.add(compra)
        db.session.commit()
        # Eager-load para devolver completa si luego se serializa
        compra = (
            db.session.query(Compra)
            .options(
                joinedload(Compra.track).joinedload(Track.usuario),
                # Si existen relaciones:
                joinedload(Compra.track).joinedload(Track.discografica),
                joinedload(Compra.track).joinedload(Track.genero),
            )
            .get(compra.idCompra)
        )
        return compra
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la compra")
        raise e

def actualizar_compra(id, data):
    compra = Compra.query.get(id)
    if not compra:
        raise ValueError("Compra no encontrada")

    fecha = validar_campos(data)
    try:
        compra.idUsuario = data['idUsuario']
        compra.idTrack = data['idTrack']
        compra.idMetodo = data['idMetodo']
        compra.fechaCompra = fecha
        compra.montoCompra = data['montoCompra']

        db.session.commit()
        compra = (
            db.session.query(Compra)
            .options(
                joinedload(Compra.track).joinedload(Track.usuario),
                joinedload(Compra.track).joinedload(Track.discografica),
                joinedload(Compra.track).joinedload(Track.genero),
            )
            .get(compra.idCompra)
        )
        return compra
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la compra")
        raise e

def eliminar_compra(id):
    compra = Compra.query.get(id)
    if not compra:
        raise ValueError("Compra no encontrada")
    try:
        db.session.delete(compra)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar la compra")
        raise e

def listar_compras(id_usuario_comprador: int):
    """
    Devuelve SOLO las compras del usuario comprador indicado.
    Pre-cargamos track + relaciones para que el front pueda mostrar artista/label/género.
    """
    q = (
        db.session.query(Compra)
        .options(
            joinedload(Compra.track).joinedload(Track.usuario),
            joinedload(Compra.track).joinedload(Track.discografica),
            joinedload(Compra.track).joinedload(Track.genero),
        )
        .filter(Compra.idUsuario == id_usuario_comprador)  # 👈 comprador
        .order_by(Compra.fechaCompra.desc())
    )
    return q.all()

def obtener_compra(id):
    compra = (
        db.session.query(Compra)
        .options(
            joinedload(Compra.track).joinedload(Track.usuario),
            joinedload(Compra.track).joinedload(Track.discografica),
            joinedload(Compra.track).joinedload(Track.genero),
        )
        .filter(Compra.idCompra == id)
        .first()
    )
    if not compra:
        raise ValueError("Compra no encontrada")
    return compra
