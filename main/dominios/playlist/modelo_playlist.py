from main.extension import db

class Playlist(db.Model):
    __tablename__ = 'playlist'

    idPlaylist = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    idDescripcionPlaylist = db.Column(db.Integer, db.ForeignKey('descripcionplaylist.idDescripcionPlaylist'), nullable=False)
    idTrack = db.Column(db.Integer, db.ForeignKey('track.idTrack'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='playlists')
    descripcion = db.relationship('DescripcionPlaylist', back_populates='playlists')
    track = db.relationship('Track', back_populates='playlists')

    def serialize(self):
        return {
            "idPlaylist": self.idPlaylist,
            "usuario": self.usuario.nombreUsuario if self.usuario else None,
            "descripcionPlaylist": self.descripcion.nombrePlaylist if self.descripcion else None,
            "track": self.track.nombreTrack if self.track else None
        }
