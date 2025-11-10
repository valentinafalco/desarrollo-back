from flask import request, jsonify
import logging
import base64
from sqlalchemy.exc import SQLAlchemyError
from main.dominios.compra.service_compra import (
    crear_compra,
    actualizar_compra,
    eliminar_compra,
    obtener_compra,
    listar_compras
)

# -------------------- HELPERS DE SERIALIZACIÓN --------------------

def _first(*vals):
    """Devuelve el primer valor no vacío/no None."""
    for v in vals:
        if v is not None and v != "":
            return v
    return None

def _as_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def _to_data_url(img_bytes):
    """Convierte bytes/bytearray a data URL base64 o deja URL/string como está."""
    if not img_bytes:
        return None
    try:
        if isinstance(img_bytes, (bytes, bytearray)):
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"  # cambia a image/png si corresponde
        if isinstance(img_bytes, str):
            return img_bytes
    except Exception:
        pass
    return None

def serialize_track(t):
    """Serializa un Track con campos habituales (tolerante a nombres distintos)."""
    if t is None:
        return None

    # Artista: priorizamos el nombre del usuario dueño del track
    artista = _first(
        getattr(getattr(t, "usuario", None), "nombreUsuario", None),  # ← usuario que subió el track
        getattr(t, "artista", None),
        getattr(t, "autor", None),
    )

    # Discográfica / Género (relación o campos sueltos)
    discografica_nombre = _first(
        getattr(getattr(t, "discografica", None), "nombreDiscografica", None),
        getattr(t, "discografica", None),
        getattr(t, "nombreDiscografica", None),
    )
    genero_nombre = _first(
        getattr(getattr(t, "genero", None), "nombreGenero", None),
        getattr(t, "genero", None),
        getattr(t, "nombreGenero", None),
    )

    # Formato / Precio
    formato = _first(
        getattr(t, "formato", None),
        getattr(t, "tipoFormato", None),
        getattr(t, "formatoAudio", None),
        getattr(t, "formatoTrack", None),
    )
    precio = _as_float(_first(
        getattr(t, "precio", None),
        getattr(t, "precioTrack", None),
        getattr(t, "precioUnitario", None),
        getattr(t, "valor", None),
        getattr(t, "monto", None),
    ), default=0.0)

    # Imagen: soporta bytes o string/URL
    portada_data = _first(
        getattr(t, "portadaURL", None),
        getattr(t, "portada", None),
        getattr(t, "imagenTrack", None),
        getattr(t, "imagen", None),
        getattr(t, "cover", None),
    )
    portada_url = _to_data_url(portada_data)

    return {
        "idTrack": _first(getattr(t, "idTrack", None), getattr(t, "id", None)),
        "nombreTrack": _first(getattr(t, "nombreTrack", None), getattr(t, "titulo", None)),
        "artista": artista,                        # 👈 ahora sale del usuario si existe
        "discografica": discografica_nombre,
        "genero": genero_nombre,
        "formato": formato,
        "precio": precio,                          # 👈 float seguro
        "portadaURL": portada_url,
    }

def serialize_compra(c):
    """Serializa una Compra e incluye el Track embebido si existe."""
    if c is None:
        return None

    fecha_compra = getattr(c, "fechaCompra", None)
    try:
        fecha_compra = fecha_compra.isoformat() if fecha_compra else None
    except Exception:
        pass

    # Tomamos precioTotal de 'montoCompra' (tu modelo) y como fallback del track
    track_obj = _first(getattr(c, "track", None), getattr(c, "Track", None))
    precio_total = _first(
        getattr(c, "montoCompra", None),           # 👈 nombre real en tu service/modelo
        getattr(c, "precioTotal", None),
        getattr(c, "monto", None),
        getattr(c, "precio", None),
        getattr(track_obj, "precio", None),        # fallback si compra no lo tiene
    )
    precio_total = _as_float(precio_total, default=0.0)

    id_track = _first(
        getattr(c, "idTrack", None),
        getattr(track_obj, "idTrack", None),
    )

    return {
        "idCompra": _first(getattr(c, "idCompra", None), getattr(c, "id", None)),
        "fechaCompra": fecha_compra,
        "precioTotal": precio_total,               # 👈 ahora llega bien
        "idUsuario": getattr(c, "idUsuario", None),
        "idTrack": id_track,
        "track": serialize_track(track_obj),
    }

# -------------------- CREAR COMPRA --------------------
def crear_compra_controller(data):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        compra = crear_compra(data)
        if not compra:
            raise ValueError("Error al crear la compra.")
        return jsonify(serialize_compra(compra)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError:
        logging.exception("Error en la base de datos al crear la compra")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception:
        logging.exception("Error inesperado al crear la compra")
        return jsonify({'error': 'Error en el servidor'}), 500

# -------------------- ACTUALIZAR COMPRA --------------------
def modificar_compra_controller(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    try:
        compra = actualizar_compra(id, data)
        return jsonify(serialize_compra(compra)), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.exception("Error al modificar la compra")
        return jsonify({'error': f'Error al modificar la compra: {str(e)}'}), 500

# -------------------- ELIMINAR COMPRA --------------------
def eliminar_compra_controller(id):
    try:
        resultado = eliminar_compra(id)
        if not resultado:
            raise ValueError("No se pudo eliminar la compra.")
        return jsonify({'mensaje': 'Compra eliminada correctamente'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al eliminar la compra")
        return jsonify({'error': f'Error al eliminar la compra: {str(e)}'}), 500

# -------------------- LISTAR COMPRAS --------------------
def listar_compras_controller():
    try:
        compras = listar_compras()  # ideal: con track y usuario ya cargados (eager loading)
        compras_serializadas = [serialize_compra(c) for c in compras]
        return jsonify(compras_serializadas), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al listar las compras")
        return jsonify({'error': f'Error al listar las compras: {str(e)}'}), 500

# -------------------- OBTENER COMPRA --------------------
def obtener_compra_controller(id):
    try:
        compra = obtener_compra(id)
        return jsonify(serialize_compra(compra)), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        logging.exception("Error al obtener la compra")
        return jsonify({'error': f'Error al obtener la compra: {str(e)}'}), 500
