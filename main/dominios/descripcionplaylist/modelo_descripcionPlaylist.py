from main.extension import db
import base64

class DescripcionPlaylist(db.Model):
    __tablename__ = 'descripcionplaylist'

    idDescripcionPlaylist = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombrePlaylist = db.Column(db.String(50), nullable=False)
    imagenPlaylist = db.Column(db.LargeBinary)
    descripcionPlaylist = db.Column(db.Text)

    playlists = db.relationship('Playlist', back_populates='descripcion', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "idDescripcionPlaylist": self.idDescripcionPlaylist,
            "nombrePlaylist": self.nombrePlaylist,
            "descripcionPlaylist": self.descripcionPlaylist,
            "imagenPlaylist": base64.b64encode(self.imagenPlaylist).decode('utf-8') if self.imagenPlaylist else None
        }
