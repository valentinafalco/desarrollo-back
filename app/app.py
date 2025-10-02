from flask import Flask, jsonify

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta de prueba
@app.route("/")
def home():
    return jsonify({"message": "Hola, Flask está funcionando 🚀"})

# Otra ruta de ejemplo
@app.route("/ping")
def ping():
    return jsonify({"response": "pong"})

if __name__ == "__main__":
    # Ejecutar la app en modo debug
    app.run(debug=True)
