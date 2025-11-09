import logging
from datetime import datetime
from main.extension import db
from main.dominios.evento.modelo_evento import Evento
from main.dominios.ubicacion.modelo_ubicacion import Ubicacion


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):
    campos_obligatorios = ['idUbicacion', 'fechaEvento', 'horarioEvento']

    # Verificar que estén todos los campos requeridos
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo]:
            raise ValueError(f"El campo {campo} no puede estar vacío")

    # Validar que la ubicación exista
    ubicacion = Ubicacion.query.get(data['idUbicacion'])
    if not ubicacion:
        raise ValueError("Ubicación no válida")

    # Validar y convertir la fecha
    try:
        fecha = datetime.strptime(data['fechaEvento'], '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Formato de fecha no válido. Use 'YYYY-MM-DD'.")

    # Validar y convertir la hora
    try:
        hora = datetime.strptime(data['horarioEvento'], '%H:%M').time()
    except ValueError:
        raise ValueError("Formato de hora no válido. Use 'HH:MM' (24h).")

    # Validar duplicado: mismo día, hora y ubicación
    evento_existente = Evento.query.filter_by(
        idUbicacion=data['idUbicacion'],
        fechaEvento=fecha,
        horarioEvento=hora
    ).first()
    if evento_existente:
        raise ValueError("Ya existe un evento en esa ubicación, fecha y hora.")

    return fecha, hora


# -------------------- CREAR EVENTO --------------------

def crear_evento(data):
    fecha, hora = validar_campos(data)

    try:
        evento = Evento(
            fechaEvento=fecha,
            horarioEvento=hora,
            idUbicacion=data['idUbicacion']
        )
        db.session.add(evento)
        db.session.commit()
        return evento
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear el evento")
        raise e


# -------------------- ACTUALIZAR EVENTO --------------------

def actualizar_evento(id, data):
    evento = Evento.query.get(id)
    if not evento:
        raise ValueError("Evento no encontrado")

    fecha, hora = validar_campos(data)

    try:
        evento.fechaEvento = fecha
        evento.horarioEvento = hora
        evento.idUbicacion = data['idUbicacion']

        db.session.commit()
        return evento
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar el evento")
        raise e


# -------------------- ELIMINAR EVENTO --------------------

def eliminar_evento(id):
    evento = Evento.query.get(id)
    if not evento:
        raise ValueError("Evento no encontrado")

    try:
        db.session.delete(evento)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar el evento")
        raise e


# -------------------- LISTAR EVENTOS --------------------

def listar_eventos():
    try:
        eventos = Evento.query.all()
        if not eventos:
            raise ValueError("No hay eventos registrados")
        return eventos
    except Exception as e:
        logging.exception("Error al listar los eventos")
        raise e


# -------------------- OBTENER EVENTO --------------------

def obtener_evento(id):
    evento = Evento.query.get(id)
    if not evento:
        raise ValueError("Evento no encontrado")
    return evento
