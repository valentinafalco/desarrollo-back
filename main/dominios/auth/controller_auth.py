# main/dominios/auth/controller_auth.py
from flask import request, jsonify
from main.dominios.auth.service_auth import login_service
import logging
import os
import jwt
from flask import request, jsonify, current_app
from main.dominios.usuario.modelo_usuario import Usuario

def login_controller():
    data = request.get_json()
    try:
        resultado = login_service(data.get('mailUsuario'), data.get('contrasenaUsuario'))
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'token': resultado['token'],
            'usuario': resultado['usuario'].serialize()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        logging.exception("Error en login")
        return jsonify({'error': 'Error en el servidor'}), 500


def me_controller():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({'error': 'Token faltante'}), 401

    token = auth.split(' ', 1)[1]
    try:
        secret = current_app.config.get('SECRET_KEY', 'clave_super_segura')  # mismo secreto
        payload = jwt.decode(token, secret, algorithms=['HS256'])

        user_id = payload.get('idUsuario')
        if not user_id:
            return jsonify({'error': 'Token inválido'}), 401

        user = Usuario.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        return jsonify(user.serialize()), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado'}), 401
    except Exception:
        logging.exception("Error en /auth/me")
        return jsonify({'error': 'Token inválido'}), 401