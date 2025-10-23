import logging
from datetime import datetime
from main.extension import db
from main.dominios.usuario.modelo_usuario import Usuario

# ---------------- VALIDAR CAMPOS ----------------
def validar_campos(data):
    campos_obligatorios = ['nombreUsuario', 'mailUsuario', 'contrasenaUsuario']
    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo requerido: {campo}")
        if not data[campo]:
            raise ValueError(f"El campo {campo} no puede estar vacío")

    if '@' not in data['mailUsuario']:
        raise ValueError("El mailUsuario debe tener un formato válido")

# ---------------- CREAR USUARIO ----------------
def crear_usuario(data):
    validar_campos(data)

    try:
        usuario = Usuario(
            nombreUsuario=data['nombreUsuario'],
            imagenUsuario=data.get('imagenUsuario'),
            descripcionUsuario=data.get('descripcionUsuario'),
            fechaCreacionUsuario=datetime.utcnow(),
            mailUsuario=data['mailUsuario']
        )

        # 🔹 Hashear antes de guardar
        usuario.set_password(data['contrasenaUsuario'])

        db.session.add(usuario)
        db.session.commit()
        return usuario

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear el usuario")
        raise e

# ---------------- ACTUALIZAR USUARIO ----------------
def actualizar_usuario(id, data):
    usuario = Usuario.query.get(id)
    if not usuario:
        raise ValueError("Usuario no encontrado")

    try:
        usuario.nombreUsuario = data.get('nombreUsuario', usuario.nombreUsuario)
        usuario.imagenUsuario = data.get('imagenUsuario', usuario.imagenUsuario)
        usuario.descripcionUsuario = data.get('descripcionUsuario', usuario.descripcionUsuario)
        usuario.mailUsuario = data.get('mailUsuario', usuario.mailUsuario)

        # 🔹 Si envían una nueva contraseña, se rehashea
        if 'contrasenaUsuario' in data and data['contrasenaUsuario']:
            usuario.set_password(data['contrasenaUsuario'])

        db.session.commit()
        return usuario

    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar el usuario")
        raise e

# ---------------- ELIMINAR USUARIO ----------------
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        raise ValueError("Usuario no encontrado")

    try:
        db.session.delete(usuario)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar el usuario")
        raise e

# ---------------- LISTAR USUARIOS ----------------
def listar_usuarios():
    try:
        usuarios = Usuario.query.all()
        if not usuarios:
            raise ValueError("No hay usuarios registrados")
        return usuarios
    except Exception as e:
        logging.exception("Error al listar los usuarios")
        raise e

# ---------------- OBTENER USUARIO ----------------
def obtener_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        raise ValueError("Usuario no encontrado")
    return usuario
