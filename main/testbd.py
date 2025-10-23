import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extension import db

# Crear la instancia de la app (esto ya inicializa db dentro de create_app)
app = create_app()

try:
    with app.app_context():
        with db.engine.connect() as conn:
            print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print("❌ Error:", e)
