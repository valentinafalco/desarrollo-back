from main.extension import db
import base64

class Evento(db.Model):
    __tablename__ = 'evento'

    idEvento = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    horarioEvento = db.Column(db.Time)
    fechaEvento = db.Column(db.Date)
    idUbicacion = db.Column(db.Integer, db.ForeignKey('ubicacion.idUbicacion'), nullable=False)

    ubicacion = db.relationship('Ubicacion', back_populates='eventos')

    def serialize(self):
        return {
            "idEvento": self.idEvento,
            "horarioEvento": self.horarioEvento.isoformat() if self.horarioEvento else None,
            "fechaEvento": self.fechaEvento.isoformat() if self.fechaEvento else None,
            "ubicacion": self.ubicacion.recintoUbicacion if self.ubicacion else None
        }
