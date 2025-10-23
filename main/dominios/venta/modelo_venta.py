from main.extension import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'venta'

    idVenta = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fechaVenta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    idTrack = db.Column(db.Integer, db.ForeignKey('track.idTrack'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='ventas')
    track = db.relationship('Track', back_populates='ventas')

    def serialize(self):
        return {
            "idVenta": self.idVenta,
            "fechaVenta": self.fechaVenta.isoformat(),
            "usuario": self.usuario.nombreUsuario if self.usuario else None,
            "track": self.track.nombreTrack if self.track else None
        }
