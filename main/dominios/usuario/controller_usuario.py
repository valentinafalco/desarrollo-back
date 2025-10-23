from flask import request, jsonify
import logging
from main.dominios.usuario.service_usuario import (
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    listar_usuarios,
    obtener_usuario
)

# ---------------- CREAR ----------------
def crear_usuario_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        usuario = crear_usuario(data)
        return jsonify(usuario.serialize()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        logging.exception("Error al crear usuario")
        return jsonify({'error': 'Error en el servidor'}), 500

# ---------------- ACTUALIZAR ----------------
def actualizar_usuario_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        usuario = actualizar_usuario(id, data)
        return jsonify(usuario.serialize()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        logging.exception("Error al actualizar usuario")
        return jsonify({'error': 'Error al actualizar usuario'}), 500

# ---------------- ELIMINAR ----------------
def eliminar_usuario_controller(id):
    try:
        resultado = eliminar_usuario(id)
        if not resultado:
            raise ValueError("No se pudo eliminar el usuario.")
        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        logging.exception("Error al eliminar usuario")
        return jsonify({'error': 'Error al eliminar usuario'}), 500

# ---------------- LISTAR ----------------
def listar_usuarios_controller():
    try:
        usuarios = listar_usuarios()
        usuarios_serializados = [u.serialize() for u in usuarios]
        return jsonify(usuarios_serializados), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        logging.exception("Error al listar usuarios")
        return jsonify({'error': 'Error al listar usuarios'}), 500

# ---------------- OBTENER ----------------
def obtener_usuario_controller(id):
    try:
        usuario = obtener_usuario(id)
        return jsonify(usuario.serialize()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        logging.exception("Error al obtener usuario")
        return jsonify({'error': 'Error al obtener usuario'}), 500
