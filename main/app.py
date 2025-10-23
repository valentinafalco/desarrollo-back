# app.py
from flask import Flask
from main.extension import db, mail
from flask_cors import CORS
from main.dominios.discografica.ruta_discografica import discografica_bp
from main.dominios.compra.ruta_compra import compra_bp
from main.dominios.genero.ruta_genero import genero_bp
from main.dominios.usuario.rutas_usuario import usuario_bp
from main.dominios.track.rutas_track import track_bp
from main.dominios.evento.rutas_evento import evento_bp
from main.dominios.ubicacion.rutas_ubicacion import ubicacion_bp
from main.dominios.metodoPago.rutas_metodoPago import metodopago_bp
from main.dominios.playlist.rutas_playlist import playlist_bp
from main.dominios.descripcionplaylist.rutas_descripcionPlaylist import descripcionplaylist_bp
from main.dominios.venta.rutas_venta import venta_bp
from main.dominios.auth.rutas_auth import auth_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    #Configuración de conexión MySQL local
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:valen1234@localhost:3306/desarrollo' 
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    app.register_blueprint(discografica_bp)
    app.register_blueprint(compra_bp)
    app.register_blueprint(genero_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(track_bp)
    app.register_blueprint(evento_bp)
    app.register_blueprint(ubicacion_bp)
    app.register_blueprint(metodopago_bp)
    app.register_blueprint(playlist_bp)
    app.register_blueprint(descripcionplaylist_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(auth_bp)
    mail.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
