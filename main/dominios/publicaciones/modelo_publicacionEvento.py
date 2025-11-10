from main.extension import db
from datetime import date

class PublicacionEvento(db.Model):
    _tablename_ = "publicacionEvento"

    idPublicacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tituloEvento = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(300))
    tipoEvento = db.Column(db.String(40))
    ubicacion = db.Column(db.String(300))
    fechaEvento = db.Column(db.Date, default=date.today)
    rutaArchivo = db.Column(db.String(255))  # imagen o video opcional

    idTrack = db.Column(db.Integer, db.ForeignKey("track.idTrack"), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)

    track = db.relationship("Track", backref="eventos")
    usuario = db.relationship("Usuario", backref="eventos")

    def serialize(self):
        return {
            "idPublicacion": self.idPublicacion,
            "tituloEvento": self.tituloEvento,
            "descripcion": self.descripcion,
            "tipoEvento": self.tipoEvento,
            "ubicacion": self.ubicacion,
            "fechaEvento": self.fechaEvento.isoformat() if self.fechaEvento else None,
            "rutaArchivo": self.rutaArchivo,
            "idTrack": self.idTrack,
            "idUsuario": self.idUsuario,
            "track": self.track.nombreTrack if self.track else None,
            "usuario": self.usuario.nombreUsuario if self.usuario else None
        }