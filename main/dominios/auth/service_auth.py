# main/dominios/auth/service_auth.py
from werkzeug.security import check_password_hash
from main.dominios.usuario.modelo_usuario import Usuario
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "clave_super_segura"

def login_service(mail, password):
    if not mail or not password:
        raise ValueError("Faltan campos obligatorios")

    usuario = Usuario.query.filter_by(mailUsuario=mail).first()
    if not usuario:
        raise ValueError("Usuario no encontrado")

    if not check_password_hash(usuario.contrasenaUsuario, password):
        raise ValueError("Contraseña incorrecta")

    token = jwt.encode({
        'idUsuario': usuario.idUsuario,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }, SECRET_KEY, algorithm='HS256')

    return {
        'token': token,
        'usuario': usuario
    }
