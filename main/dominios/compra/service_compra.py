import logging
from datetime import datetime
from main.extension import db
from main.dominios.compra.modelo_compra import Compra
from main.dominios.usuario.modelo_usuario import Usuario
from main.dominios.track.modelo_track import Track
from main.dominios.metodoPago.modelo_metodoPago import MetodoPago_Usuario

#Validaciones de los campos de entrada
def validar_campos(data):
    campos_obligatorios = ['idUsuario', 'idTrack', 'idMetodo', 'fechaCompra', 'montoCompra']

    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo]:
            raise ValueError(f"El campo {campo} no puede estar vacío")

    #Validar tipos y formato de fecha
    try:
        fecha = datetime.strptime(data['fechaCompra'], '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("El formato de fecha debe ser YYYY-MM-DD")

    if not isinstance(data['montoCompra'], (int, float)):
        raise ValueError("El montoCompra debe ser numérico")

    #Validar existencia de claves foráneas
    if not Usuario.query.get(data['idUsuario']):
        raise ValueError("Usuario no válido")

    if not Track.query.get(data['idTrack']):
        raise ValueError("Track no válido")

    if not MetodoPago.query.get(data['idMetodo']):
        raise ValueError("Método de pago no válido")

    return fecha


#Crear una compra
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
        return compra
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la compra")
        raise e


#Actualizar una compra existente
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
        return compra
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la compra")
        raise e


#Eliminar una compra
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


#Listar todas las compras
def listar_compras():
    try:
        compras = Compra.query.all()
        if not compras:
            raise ValueError("No hay compras registradas")
        return compras
    except Exception as e:
        logging.exception("Error al listar las compras")
        raise e


#Obtener una compra específica
def obtener_compra(id):
    compra = Compra.query.get(id)
    if not compra:
        raise ValueError("Compra no encontrada")
    return compra
