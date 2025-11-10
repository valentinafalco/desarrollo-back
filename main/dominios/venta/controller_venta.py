from flask import request, jsonify, current_app
import logging, os, jwt
from sqlalchemy.exc import SQLAlchemyError

from main.dominios.venta.service_venta import (
    crear_venta,
    actualizar_venta,
    eliminar_venta,
    listar_ventas as service_listar_ventas,
    obtener_venta
)

# -------- Helpers de serialización --------

import base64

def _first(*vals):
    for v in vals:
        if v is not None and v != "":
            return v
    return None

def _as_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def _to_data_url(img_bytes_or_str):
    if not img_bytes_or_str:
        return None
    # si ya es str, puede ser URL o dataURL o base64 plano
    if isinstance(img_bytes_or_str, str):
        if img_bytes_or_str.startswith("http") or img_bytes_or_str.startswith("data:"):
            return img_bytes_or_str
        # si parece base64 sin prefijo:
        try:
            # validamos decodificación
            base64.b64decode(img_bytes_or_str, validate=True)
            return f"data:image/jpeg;base64,{img_bytes_or_str}"
        except Exception:
            return img_bytes_or_str
    # si son bytes -> data URL
    if isinstance(img_bytes_or_str, (bytes, bytearray)):
        try:
            b64 = base64.b64encode(img_bytes_or_str).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"
        except Exception:
            return None
    return None

def _serialize_track_public(t):
    if t is None:
        return None

    artista = _first(
        getattr(getattr(t, "usuario", None), "nombreUsuario", None),  # dueño del track
        getattr(t, "artista", None),
        getattr(t, "autor", None),
        "Desconocido",
    )

    discografica_nombre = _first(
        getattr(getattr(t, "discografica", None), "nombreDiscografica", None),
        getattr(t, "discografica", None),
    )
    genero_nombre = _first(
        getattr(getattr(t, "genero", None), "nombreGenero", None),
        getattr(t, "genero", None),
    )

    formato = _first(getattr(t, "formato", None), getattr(t, "formatoTrack", None))
    precio  = _as_float(_first(getattr(t, "precio", None), getattr(t, "precioTrack", None)), 0.0)

    portada_url = _first(
        getattr(t, "portadaURL", None),
        _to_data_url(getattr(t, "imagenTrack", None)),
    )

    return {
        "idTrack": _first(getattr(t, "idTrack", None), getattr(t, "id", None)),
        "nombreTrack": _first(getattr(t, "nombreTrack", None), getattr(t, "titulo", None)),
        "artista": artista,
        "discografica": discografica_nombre,
        "genero": genero_nombre,
        "formato": formato,
        "precio": precio,
        "portadaURL": portada_url,
        # opcional: exponer el usuario dueño
        "usuario": {
            "idUsuario": _first(
                getattr(getattr(t, "usuario", None), "idUsuario", None),
                getattr(t, "idUsuario", None)
            ),
            "nombreUsuario": getattr(getattr(t, "usuario", None), "nombreUsuario", None)
        }
    }

def _serialize_venta_from_compra(c):
    """
    Serializa una 'venta' a partir de una Compra (derivada): incluye track embebido.
    """
    if c is None:
        return None

    fecha = getattr(c, "fechaCompra", None)
    try:
        fecha = fecha.isoformat() if fecha else None
    except Exception:
        pass

    t = getattr(c, "track", None)

    return {
        # mantenemos ids por si luego tenés tabla Venta real
        "idVenta": _first(getattr(c, "idVenta", None), getattr(c, "id", None)),
        "idCompra": getattr(c, "idCompra", None),
        "fechaVenta": fecha or getattr(c, "fecha", None),
        "precioTotal": _as_float(
            _first(
                getattr(c, "montoCompra", None),
                getattr(c, "precioTotal", None),
                getattr(c, "monto", None),
                getattr(t, "precio", None),
                getattr(t, "precioTrack", None),
            ), 0.0
        ),
        "idUsuarioComprador": getattr(c, "idUsuario", None),  # quien compró
        "track": _serialize_track_public(t),                  # lo que vendés
    }


# -------------------- CREAR VENTA (tabla Venta) --------------------
def crear_venta_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        venta = crear_venta(data)
        if not venta:
            raise ValueError("Error al crear la venta.")
        return jsonify(venta.serialize()), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al crear la venta")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ACTUALIZAR VENTA (tabla Venta) --------------------
def modificar_venta_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        venta = actualizar_venta(id, data)
        return jsonify(venta.serialize()), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al modificar la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al modificar la venta")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- ELIMINAR VENTA (tabla Venta) --------------------
def eliminar_venta_controller(id):
    try:
        resultado = eliminar_venta(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la venta.")
        return jsonify({'mensaje': 'Venta eliminada correctamente'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al eliminar la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al eliminar la venta")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- LISTAR VENTAS (derivadas de compras) --------------------
def _user_id_from_token():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ', 1)[1]
    try:
        secret = current_app.config.get('SECRET_KEY', 'clave_super_segura')
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload.get('idUsuario')
    except Exception:
        return None

def _serialize_venta_from_compra(c):
    # Reutilizamos el mismo formato que en compras, porque la fuente es Compra
    t = getattr(c, "track", None)
    return {
        "idVenta": getattr(c, "idCompra", None),  # id de la compra como id lógico de venta
        "fechaVenta": c.fechaCompra.isoformat() if c.fechaCompra else None,
        "precioTotal": float(getattr(c, "montoCompra", 0) or getattr(t, "precioTrack", 0) or 0),
        "idUsuarioComprador": c.idUsuario,
        "idTrack": getattr(t, "idTrack", getattr(c, "idTrack", None)),
        "track": None if not t else {
            "idTrack": t.idTrack,
            "nombreTrack": getattr(t, "nombreTrack", None),
            "usuario": {
                "idUsuario": getattr(getattr(t, "usuario", None), "idUsuario", None),
                "nombreUsuario": getattr(getattr(t, "usuario", None), "nombreUsuario", None)
            },
            "discografica": {
                "nombreDiscografica": getattr(getattr(t, "discografica", None), "nombreDiscografica", None)
            } if getattr(t, "discografica", None) else None,
            "genero": {
                "nombreGenero": getattr(getattr(t, "genero", None), "nombreGenero", None)
            } if getattr(t, "genero", None) else None,
            "precioTrack": float(getattr(t, "precioTrack", 0) or 0),
            "formatoTrack": getattr(t, "formatoTrack", None),
        }
    }

def listar_ventas_controller():
    """
    GET /ventas?idUsuario=X -> ventas del VENDEDOR X (dueño del track)
    Si no viene idUsuario, lo toma del token.
    """
    try:
        id_usuario_vendedor = request.args.get("idUsuario", type=int)
        if not id_usuario_vendedor:
            id_usuario_vendedor = _user_id_from_token()
        if not id_usuario_vendedor:
            return jsonify({'error': 'idUsuario (vendedor) es requerido'}), 400

        compras_de_mis_tracks = service_listar_ventas(id_usuario_vendedor=id_usuario_vendedor)
        payload = [_serialize_venta_from_compra(c) for c in compras_de_mis_tracks]
        return jsonify(payload), 200

    except SQLAlchemyError:
        logging.exception("Error en la base de datos al listar las ventas")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al listar las ventas")
        return jsonify({'error': 'Error en el servidor'}), 500


# -------------------- OBTENER VENTA (tabla Venta) --------------------
def obtener_venta_controller(id):
    try:
        venta = obtener_venta(id)
        return jsonify(venta.serialize()), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al obtener la venta")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al obtener la venta")
        return jsonify({'error': 'Error en el servidor'}), 500
