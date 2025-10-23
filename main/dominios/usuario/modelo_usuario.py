from main.extension import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreUsuario = db.Column(db.String(100), nullable=False)
    imagenUsuario = db.Column(db.LargeBinary, nullable=True)
    descripcionUsuario = db.Column(db.Text)
    fechaCreacionUsuario = db.Column(db.DateTime, default=datetime.utcnow)
    mailUsuario = db.Column(db.String(255), unique=True, nullable=False)
    contrasenaUsuario = db.Column(db.String(255), nullable=False)  # 🔹 se mantiene este nombre

    # Relaciones
    metodos_pago = db.relationship('MetodoPago_Usuario', back_populates='usuario', cascade='all, delete-orphan')
    tracks = db.relationship('Track', back_populates='usuario', cascade='all, delete-orphan')
    ventas = db.relationship('Venta', back_populates='usuario', cascade='all, delete-orphan')
    compras = db.relationship('Compra', back_populates='usuario', cascade='all, delete-orphan')
    playlists = db.relationship('Playlist', back_populates='usuario', cascade='all, delete-orphan')

    # ------- Métodos para manejo seguro de contraseñas -------
    def set_password(self, contrasena_plana):
        #Genera el hash y lo guarda en el mismo campo contrasenaUsuario
        self.contrasenaUsuario = generate_password_hash(contrasena_plana)

    def check_password(self, contrasena_plana):
        #Verifica si una contraseña coincide con el hash almacenado
        return check_password_hash(self.contrasenaUsuario, contrasena_plana)

    def serialize(self):
        return {
            "idUsuario": self.idUsuario,
            "nombreUsuario": self.nombreUsuario,
            "descripcionUsuario": self.descripcionUsuario,
            "fechaCreacionUsuario": self.fechaCreacionUsuario.isoformat() if self.fechaCreacionUsuario else None,
            "mailUsuario": self.mailUsuario
        }
