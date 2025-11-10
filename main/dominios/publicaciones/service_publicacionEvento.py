from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.publicaciones.service_publicacionEvento import (
    crear_publicacion_evento,
    listar_publicaciones_evento,
    obtener_publicacion_evento,
    eliminar_publicacion_evento
)
import logging

# -------------------- CREAR --------------------
def crear_publicacion_evento_controller():
    try:
        data = request.form.to_dict()
        archivo = request.files.get("archivo")
        publicacion = crear_publicacion_evento(data, archivo)
        return jsonify(publicacion.serialize()), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except SQLAlchemyError:
        logging.exception("Error en la base de datos")
        return jsonify({"error": "Error en la base de datos"}), 500
    except Exception as e:
        logging.exception("Error al crear publicación")
        return jsonify({"error": str(e)}), 500


# -------------------- LISTAR --------------------
def listar_publicaciones_evento_controller():
    try:
        publicaciones = listar_publicaciones_evento()
        return jsonify([p.serialize() for p in publicaciones]), 200
    except Exception as e:
        logging.exception("Error al listar publicaciones")
        return jsonify({"error": str(e)}), 500


# -------------------- OBTENER POR ID --------------------
def obtener_publicacion_evento_controller(id):
    try:
        p = obtener_publicacion_evento(id)
        return jsonify(p.serialize()), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.exception("Error al obtener publicación")
        return jsonify({"error": str(e)}), 500


# -------------------- ELIMINAR --------------------
def eliminar_publicacion_evento_controller(id):
    try:
        eliminar_publicacion_evento(id)
        return jsonify({"mensaje": "Publicación eliminada correctamente"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.exception("Error al eliminar publicación")
        return jsonify({"error": str(e)}), 500