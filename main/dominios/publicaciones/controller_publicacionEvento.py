from flask import request, jsonify, url_for, Response
import logging
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.publicaciones.service_publicacionEvento import (
    crear_publicacion_evento,
    actualizar_publicacion_evento,
    eliminar_publicacion_evento,
    listar_publicaciones_evento,
    obtener_publicacion_evento
)


# -------------------- CREAR --------------------
def crear_publicacion_evento_controller():
    data = request.form.to_dict()
    archivo = request.files.get("archivo")  

    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400

    try:
        publicacion = crear_publicacion_evento(data, archivo)
        respuesta = publicacion.serialize()
        if publicacion.imagen:
            respuesta["imagenUrl"] = url_for(
                "publicacion_evento_bp.obtener_imagen_publicacion",
                id=publicacion.idPublicacion,
                _external=True
            )
        return jsonify(respuesta), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la publicación")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al crear la publicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR --------------------
def modificar_publicacion_evento_controller(id):
    data = request.form.to_dict()
    archivo = request.files.get("archivo")

    try:
        publicacion = actualizar_publicacion_evento(id, data, archivo)
        respuesta = publicacion.serialize()
        if publicacion.imagen:
            respuesta["imagenUrl"] = url_for(
                "publicacion_evento_bp.obtener_imagen_publicacion",
                id=publicacion.idPublicacion,
                _external=True
            )
        return jsonify(respuesta), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al actualizar la publicación")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al actualizar la publicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR --------------------
def eliminar_publicacion_evento_controller(id):
    try:
        eliminar_publicacion_evento(id)
        return jsonify({'mensaje': 'Publicación eliminada correctamente'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception:
        logging.exception("Error al eliminar publicación")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR --------------------
def listar_publicaciones_evento_controller():
    try:
        publicaciones = listar_publicaciones_evento()
        lista = []
        for p in publicaciones:
            data = p.serialize()
            if p.imagen:
                data["imagenUrl"] = url_for(
                    "publicacion_evento_bp.obtener_imagen_publicacion",
                    id=p.idPublicacion,
                    _external=True
                )
            lista.append(data)
        return jsonify(lista), 200
    except Exception as e:
        logging.exception("Error al listar publicaciones")
        return jsonify({'error': str(e)}), 500


# -------------------- OBTENER --------------------
def obtener_publicacion_evento_controller(id):
    try:
        p = obtener_publicacion_evento(id)
        data = p.serialize()
        if p.imagen:
            data["imagenUrl"] = url_for(
                "publicacion_evento_bp.obtener_imagen_publicacion",
                id=p.idPublicacion,
                _external=True
            )
        return jsonify(data), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al obtener publicación")
        return jsonify({'error': str(e)}), 500


# -------------------- SERVIR IMAGEN --------------------
def obtener_imagen_publicacion_controller(id):
    try:
        publicacion = obtener_publicacion_evento(id)
        if not publicacion.imagen:
            return jsonify({'error': 'Esta publicación no tiene imagen'}), 404
        return Response(publicacion.imagen, mimetype='image/jpeg')
    except Exception:
        logging.exception("Error al obtener imagen")
        return jsonify({'error': 'Error en el servidor'}), 500
