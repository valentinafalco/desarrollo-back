from main.extension import db
import base64 	# Para codificar la imagen en base64 al serializar

class Discografica(db.Model):
    __tablename__ = 'discografica'

    idDiscografica = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreDiscografica = db.Column(db.String(50), nullable=False)
    imagenDiscografica = db.Column(db.LargeBinary)
    descripcionDiscografica = db.Column(db.Text)

    # Relación con Track
    tracks = db.relationship('Track', back_populates='discografica', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "idDiscografica": self.idDiscografica,
            "nombreDiscografica": self.nombreDiscografica,
            "descripcionDiscografica": self.descripcionDiscografica,
            "imagenDiscografica": base64.b64encode(self.imagenDiscografica).decode('utf-8') if self.imagenDiscografica else None
        }

