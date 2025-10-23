# main/dominios/auth/controller_auth.py
from flask import request, jsonify
from main.dominios.auth.service_auth import login_service
import logging

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
