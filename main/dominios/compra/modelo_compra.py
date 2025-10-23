from main.extension import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compra'

    idCompra = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fechaCompra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    montoCompra = db.Column(db.Numeric(10, 2), nullable=False)

    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    idTrack = db.Column(db.Integer, db.ForeignKey('track.idTrack'), nullable=False)
    idMetodo = db.Column(db.Integer, db.ForeignKey('metodopago_usuario.idMetodo'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='compras')
    track = db.relationship('Track', back_populates='compras')
    metodo = db.relationship('MetodoPago_Usuario', back_populates='compras')

    def serialize(self):
        return {
            "idCompra": self.idCompra,
            "fechaCompra": self.fechaCompra.isoformat(),
            "montoCompra": float(self.montoCompra),
            "usuario": self.usuario.nombreUsuario if self.usuario else None,
            "track": self.track.nombreTrack if self.track else None,
            "metodo": self.metodo.proveedorPago if self.metodo else None
        }
