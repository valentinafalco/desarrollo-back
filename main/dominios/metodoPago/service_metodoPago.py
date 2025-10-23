import logging
from main.extension import db
from main.dominios.metodoPago.modelo_metodoPago import MetodoPago_Usuario
from main.dominios.usuario.modelo_usuario import Usuario


# -------------------- VALIDAR CAMPOS --------------------

def validar_campos(data):
    campos_obligatorios = ['idUsuario', 'tokenPago', 'proveedorPago']

    # Verificar presencia de todos los campos
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if data[campo] in (None, ""):
            raise ValueError(f"El campo '{campo}' no puede estar vacío")

    # Validar existencia del usuario
    if not Usuario.query.get(data['idUsuario']):
        raise ValueError("Usuario no válido")

    # Validar longitudes máximas
    if len(data['tokenPago']) > 50:
        raise ValueError("El campo 'tokenPago' no puede superar los 50 caracteres")

    if len(data['proveedorPago']) > 50:
        raise ValueError("El campo 'proveedorPago' no puede superar los 50 caracteres")

    return True


# -------------------- CREAR MÉTODO DE PAGO --------------------

def crear_metodo_pago(data):
    validar_campos(data)

    try:
        metodo = MetodoPago_Usuario(
            idUsuario=data['idUsuario'],
            tokenPago=data['tokenPago'].strip(),
            proveedorPago=data['proveedorPago'].strip()
        )
        db.session.add(metodo)
        db.session.commit()
        return metodo
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear el método de pago")
        raise e


# -------------------- ACTUALIZAR MÉTODO DE PAGO --------------------

def actualizar_metodo_pago(id, data):
    metodo = MetodoPago_Usuario.query.get(id)
    if not metodo:
        raise ValueError("Método de pago no encontrado")

    validar_campos(data)

    try:
        metodo.idUsuario = data['idUsuario']
        metodo.tokenPago = data['tokenPago'].strip()
        metodo.proveedorPago = data['proveedorPago'].strip()

        db.session.commit()
        return metodo
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar el método de pago")
        raise e


# -------------------- ELIMINAR MÉTODO DE PAGO --------------------

def eliminar_metodo_pago(id):
    metodo = MetodoPago_Usuario.query.get(id)
    if not metodo:
        raise ValueError("Método de pago no encontrado")

    try:
        db.session.delete(metodo)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar el método de pago")
        raise e


# -------------------- LISTAR MÉTODOS DE PAGO --------------------

def listar_metodos_pago():
    try:
        metodos = MetodoPago_Usuario.query.all()
        if not metodos:
            raise ValueError("No hay métodos de pago registrados")
        return metodos
    except Exception as e:
        logging.exception("Error al listar los métodos de pago")
        raise e


# -------------------- OBTENER MÉTODO DE PAGO --------------------

def obtener_metodo_pago(id):
    metodo = MetodoPago_Usuario.query.get(id)
    if not metodo:
        raise ValueError("Método de pago no encontrado")
    return metodo
