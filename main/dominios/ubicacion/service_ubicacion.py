import logging
from main.extension import db
from main.dominios.ubicacion.modelo_ubicacion import Ubicacion


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):

    campos_obligatorios = ['numeroUbicacion', 'calleUbicacion', 'provinciaUbicacion', 'ciudadUbicacion', 'recintoUbicacion']

    # Verificar presencia y contenido de los campos
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if data[campo] in (None, ""):
            raise ValueError(f"El campo '{campo}' no puede estar vacío")

    # Validar tipo numérico
    if not isinstance(data['numeroUbicacion'], int):
        raise ValueError("El campo 'numeroUbicacion' debe ser un número entero")

    # Validar longitud de cadenas
    for campo_texto in ['calleUbicacion', 'provinciaUbicacion', 'ciudadUbicacion', 'recintoUbicacion']:
        if len(data[campo_texto]) > 100:
            raise ValueError(f"El campo '{campo_texto}' no puede superar los 100 caracteres")

    return True


# -------------------- CREAR UBICACIÓN --------------------

def crear_ubicacion(data):
    validar_campos(data)

    try:
        ubicacion = Ubicacion(
            numeroUbicacion=data['numeroUbicacion'],
            calleUbicacion=data['calleUbicacion'].strip(),
            provinciaUbicacion=data['provinciaUbicacion'].strip(),
            ciudadUbicacion=data['ciudadUbicacion'].strip(),
            recintoUbicacion=data['recintoUbicacion'].strip()
        )
        db.session.add(ubicacion)
        db.session.commit()
        return ubicacion
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear la ubicación")
        raise e


# -------------------- ACTUALIZAR UBICACIÓN --------------------

def actualizar_ubicacion(id, data):
    ubicacion = Ubicacion.query.get(id)
    if not ubicacion:
        raise ValueError("Ubicación no encontrada")

    validar_campos(data)

    try:
        ubicacion.numeroUbicacion = data['numeroUbicacion']
        ubicacion.calleUbicacion = data['calleUbicacion'].strip()
        ubicacion.provinciaUbicacion = data['provinciaUbicacion'].strip()
        ubicacion.ciudadUbicacion = data['ciudadUbicacion'].strip()
        ubicacion.recintoUbicacion = data['recintoUbicacion'].strip()

        db.session.commit()
        return ubicacion
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar la ubicación")
        raise e


# -------------------- ELIMINAR UBICACIÓN --------------------

def eliminar_ubicacion(id):
    ubicacion = Ubicacion.query.get(id)
    if not ubicacion:
        raise ValueError("Ubicación no encontrada")

    try:
        db.session.delete(ubicacion)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar la ubicación")
        raise e


# -------------------- LISTAR UBICACIONES --------------------

def listar_ubicaciones():
    try:
        ubicaciones = Ubicacion.query.all()
        if not ubicaciones:
            raise ValueError("No hay ubicaciones registradas")
        return ubicaciones
    except Exception as e:
        logging.exception("Error al listar las ubicaciones")
        raise e


# -------------------- OBTENER UBICACIÓN --------------------

def obtener_ubicacion(id):
    ubicacion = Ubicacion.query.get(id)
    if not ubicacion:
        raise ValueError("Ubicación no encontrada")
    return ubicacion
