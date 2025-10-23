from main.extension import db
import base64

class Track(db.Model):
    __tablename__ = 'track'

    idTrack = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreTrack = db.Column(db.String(50), nullable=False)
    bpm = db.Column(db.Integer)
    duracion = db.Column(db.Time)
    formatoTrack = db.Column(db.String(50))
    precioTrack = db.Column(db.Float)
    fechaLanzamiento = db.Column(db.Date)
    imagenTrack = db.Column(db.LargeBinary)
    favoritosTrack = db.Column(db.Integer, default=0)
    reproduccionesTrack = db.Column(db.Integer, default=0)

    idDiscografica = db.Column(db.Integer, db.ForeignKey('discografica.idDiscografica'))
    idGenero = db.Column(db.Integer, db.ForeignKey('genero.idGenero'))
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))

    # Relaciones
    discografica = db.relationship('Discografica', back_populates='tracks')
    genero = db.relationship('Genero', back_populates='tracks')
    usuario = db.relationship('Usuario', back_populates='tracks')
    ventas = db.relationship('Venta', back_populates='track', cascade='all, delete-orphan')
    compras = db.relationship('Compra', back_populates='track', cascade='all, delete-orphan')
    playlists = db.relationship('Playlist', back_populates='track', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "idTrack": self.idTrack,
            "nombreTrack": self.nombreTrack,
            "bpm": self.bpm,
            "duracion": str(self.duracion) if self.duracion else None,
            "precioTrack": self.precioTrack,
            "fechaLanzamiento": self.fechaLanzamiento.isoformat() if self.fechaLanzamiento else None
        }
