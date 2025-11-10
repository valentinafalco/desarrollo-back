# main/dominios/auth/rutas_auth.py
from flask import Blueprint
from main.dominios.auth.controller_auth import login_controller, me_controller

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_controller()

@auth_bp.route('/me', methods=['GET'])
def me():
    return me_controller()
