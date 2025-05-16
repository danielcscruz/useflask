from flask import jsonify, request
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def register():
    """Endpoint para registrar um novo usuário"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
            
        username = data.get("username")
        password = data.get("password")
        
        # Verificações básicas
        if not username or not password:
            return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400
        
        # Verifica se o usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Usuário já existe"}), 400

        # Cria o novo usuário
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_pw)
        
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuário registrado com sucesso", "user_id": user.id}), 201
    
    except Exception as e:
        db.session.rollback()  # Reverte operações em caso de erro
        return jsonify({"error": f"Erro ao registrar: {str(e)}"}), 500

def login():
    """Endpoint para fazer login e receber token JWT"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
            
        username = data.get("username")
        password = data.get("password")
        
        # Verificações básicas
        if not username or not password:
            return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400

        # Busca o usuário e verifica credenciais
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Credenciais inválidas"}), 401

        # Cria token JWT
        token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": token,
            "user_id": user.id,
            "username": user.username
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao fazer login: {str(e)}"}), 500

@jwt_required()
def protected():
    """Endpoint protegido que requer autenticação JWT"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        return jsonify({
            "message": f"Bem-vindo, {user.username}!",
            "user_id": user.id
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro: {str(e)}"}), 500