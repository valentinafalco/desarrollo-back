import logging
from datetime import datetime
from main.extension import db
from main.dominios.publicaciones.modelo_publicacionEvento import PublicacionEvento
from main.dominios.usuario.modelo_usuario import Usuario
from main.dominios.track.modelo_track import Track   # ajustá el path si difiere


# -------------------- VALIDAR CAMPOS --------------------
def _validar_campos(data, parcial=False):
    """
    Si parcial=True permite updates parciales (PATCH-like).
    Si parcial=False exige todos los obligatorios (POST/PUT).
    """
    obligatorios = ['tituloEvento', 'tipoEvento', 'fechaEvento', 'idUsuario', 'idTrack']
    if not parcial:
        for campo in obligatorios:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido: {campo}")
            if data[campo] in (None, ""):
                raise ValueError(f"El campo '{campo}' no puede estar vacío")
    else:
        # si viene, que no sea vacío
        for k, v in data.items():
            if v in (None, ""):
                raise ValueError(f"El campo '{k}' no puede estar vacío")

    # Validaciones de longitudes (solo si vienen)
    if 'tituloEvento' in data and len(data['tituloEvento']) > 50:
        raise ValueError("El campo 'tituloEvento' no puede superar los 50 caracteres")
    if 'tipoEvento' in data and len(data['tipoEvento']) > 40:
        raise ValueError("El campo 'tipoEvento' no puede superar los 40 caracteres")
    if 'ubicacion' in data and data['ubicacion'] is not None and len(data['ubicacion']) > 300:
        raise ValueError("El campo 'ubicacion' no puede superar los 300 caracteres")
    if 'descripcion' in data and data['descripcion'] is not None and len(data['descripcion']) > 300:
        raise ValueError("El campo 'descripcion' no puede superar los 300 caracteres")

    # Validación de fecha (YYYY-MM-DD)
    if 'fechaEvento' in data:
        try:
            datetime.strptime(data['fechaEvento'], "%Y-%m-%d")
        except ValueError:
            raise ValueError("El campo 'fechaEvento' debe tener formato YYYY-MM-DD")

    # Validación de FKs (solo si vienen)
    if 'idUsuario' in data:
        if not Usuario.query.get(data['idUsuario']):
            raise ValueError("Usuario no válido")
    if 'idTrack' in data:
        if not Track.query.get(data['idTrack']):
            raise ValueError("Track no válido")

    return True


# -------------------- CREAR --------------------
def crear_publicacion_evento(data: dict):
    _validar_campos(data, parcial=False)
    try:
        publicacion = PublicacionEvento(
            tituloEvento=data['tituloEvento'].strip(),
            descripcion=(data.get('descripcion') or "").strip() or None,
            tipoEvento=data['tipoEvento'].strip(),
            ubicacion=(data.get('ubicacion') or "").strip() or None,
            fechaEvento=data['fechaEvento'],    # string YYYY-MM-DD (SQLAlchemy Date lo castea)
            idTrack=data['idTrack'],
            idUsuario=data['idUsuario'],
        )
        db.session.add(publicacion)
        db.session.commit()
        return publicacion
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al crear publicación de evento")
        raise e


# -------------------- ACTUALIZAR --------------------
def actualizar_publicacion_evento(id: int, data: dict):
    publicacion = PublicacionEvento.query.get(id)
    if not publicacion:
        raise ValueError("Publicación no encontrada")

    _validar_campos(data, parcial=True)

    try:
        if 'tituloEvento' in data:
            publicacion.tituloEvento = data['tituloEvento'].strip()
        if 'descripcion' in data:
            publicacion.descripcion = (data.get('descripcion') or "").strip() or None
        if 'tipoEvento' in data:
            publicacion.tipoEvento = data['tipoEvento'].strip()
        if 'ubicacion' in data:
            publicacion.ubicacion = (data.get('ubicacion') or "").strip() or None
        if 'fechaEvento' in data:
            publicacion.fechaEvento = data['fechaEvento']
        if 'idTrack' in data:
            publicacion.idTrack = data['idTrack']
        if 'idUsuario' in data:
            publicacion.idUsuario = data['idUsuario']

        db.session.commit()
        return publicacion
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al actualizar publicación de evento")
        raise e


# -------------------- ELIMINAR --------------------
def eliminar_publicacion_evento(id: int):
    publicacion = PublicacionEvento.query.get(id)
    if not publicacion:
        raise ValueError("Publicación no encontrada")

    try:
        db.session.delete(publicacion)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.exception("Error al eliminar publicación de evento")
        raise e


# -------------------- LISTAR --------------------
def listar_publicaciones_evento():
    try:
        publicaciones = PublicacionEvento.query.all()
        if not publicaciones:
            # mantener la semántica del ejemplo de metodoPago
            raise ValueError("No hay publicaciones registradas")
        return publicaciones
    except Exception as e:
        logging.exception("Error al listar publicaciones")
        raise e


# -------------------- OBTENER POR ID --------------------
def obtener_publicacion_evento(id: int):
    publicacion = PublicacionEvento.query.get(id)
    if not publicacion:
        raise ValueError("Publicación no encontrada")
    return publicacion
