from main.extension import db

class MetodoPago_Usuario(db.Model):
    __tablename__ = 'metodopago_usuario'

    idMetodo = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    tokenPago = db.Column(db.String(50))
    proveedorPago = db.Column(db.String(50))

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='metodos_pago')
    compras = db.relationship('Compra', back_populates='metodo', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "idMetodo": self.idMetodo,
            "tokenPago": self.tokenPago,
            "proveedorPago": self.proveedorPago,
            "usuario": self.usuario.nombreUsuario if self.usuario else None
        }

