from main.extension import db

class Genero(db.Model):
    __tablename__ = 'genero'

    idGenero = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreGenero = db.Column(db.String(100), nullable=False)

    # Relación con Track
    tracks = db.relationship('Track', back_populates='genero', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "idGenero": self.idGenero,
            "nombreGenero": self.nombreGenero
        }

