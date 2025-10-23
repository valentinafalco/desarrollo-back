from main.extension import db

class Ubicacion(db.Model):
    __tablename__ = 'ubicacion'

    idUbicacion = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    numeroUbicacion = db.Column(db.Integer)
    calleUbicacion = db.Column(db.String(100))
    provinciaUbicacion = db.Column(db.String(100))
    ciudadUbicacion = db.Column(db.String(100))
    recintoUbicacion = db.Column(db.String(100))

    # Relación con Evento (uno a muchos)
    eventos = db.relationship('Evento', back_populates='ubicacion', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "idUbicacion": self.idUbicacion,
            "numeroUbicacion": self.numeroUbicacion,
            "calleUbicacion": self.calleUbicacion,
            "provinciaUbicacion": self.provinciaUbicacion,
            "ciudadUbicacion": self.ciudadUbicacion,
            "recintoUbicacion": self.recintoUbicacion
        }
