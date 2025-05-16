from flask import Blueprint, jsonify
from app.auth import register, login, protected

# Criação do blueprint de autenticação
auth_bp = Blueprint("auth", __name__)

# Rotas de autenticação
auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/protected", methods=["GET"])(protected)

# Rota para testar se a API está funcionando
@auth_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando!"}), 200