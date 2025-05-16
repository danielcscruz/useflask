from flask import Blueprint, jsonify, request
from app import db
from app.models import Script, User
from flask_jwt_extended import jwt_required, get_jwt_identity

# Criação do blueprint para scripts
scripts_bp = Blueprint("scripts", __name__)

@scripts_bp.route("/", methods=["GET"])
@jwt_required()
def get_scripts():
    """Recupera todos os scripts do usuário atual"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        # Recupera scripts associados ao usuário
        scripts = user.scripts.all()
        
        result = []
        for script in scripts:
            result.append({
                "id": script.id,
                "title": script.title,
                "description": script.description,
                "created_at": script.created_at.isoformat(),
                "updated_at": script.updated_at.isoformat()
            })
            
        return jsonify({"scripts": result}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar scripts: {str(e)}"}), 500

@scripts_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_scripts():
    """Recupera todos os scripts do sistema"""
    try:
        scripts = Script.query.all()
        
        result = []
        for script in scripts:
            result.append({
                "id": script.id,
                "title": script.title,
                "description": script.description,
                "created_at": script.created_at.isoformat(),
                "updated_at": script.updated_at.isoformat()
            })
            
        return jsonify({"scripts": result}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar scripts: {str(e)}"}), 500

@scripts_bp.route("/<int:script_id>", methods=["GET"])
@jwt_required()
def get_script(script_id):
    """Recupera um script específico pelo ID"""
    try:
        script = Script.query.get(script_id)
        
        if not script:
            return jsonify({"error": "Script não encontrado"}), 404
            
        # Verifica se o usuário tem acesso ao script
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Se o usuário não estiver associado ao script, não mostra o conteúdo completo
        is_associated = user.scripts.filter_by(id=script_id).first() is not None
        
        script_data = {
            "id": script.id,
            "title": script.title,
            "description": script.description,
            "created_at": script.created_at.isoformat(),
            "updated_at": script.updated_at.isoformat()
        }
        
        # Só inclui o conteúdo se o usuário tiver acesso
        if is_associated:
            script_data["content"] = script.content
            
        return jsonify({"script": script_data}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar script: {str(e)}"}), 500

@scripts_bp.route("/", methods=["POST"])
@jwt_required()
def create_script():
    """Cria um novo script e associa ao usuário atual"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
            
        title = data.get("title")
        content = data.get("content")
        description = data.get("description", "")
        
        # Validação básica
        if not title or not content:
            return jsonify({"error": "Título e conteúdo são obrigatórios"}), 400
        
        # Cria o novo script
        script = Script(
            title=title,
            content=content,
            description=description
        )
        
        # Associa ao usuário atual
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        user.scripts.append(script)
        
        db.session.add(script)
        db.session.commit()
        
        return jsonify({
            "message": "Script criado com sucesso",
            "script_id": script.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar script: {str(e)}"}), 500

@scripts_bp.route("/<int:script_id>", methods=["PUT"])
@jwt_required()
def update_script(script_id):
    """Atualiza um script existente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
            
        # Busca o script
        script = Script.query.get(script_id)
        if not script:
            return jsonify({"error": "Script não encontrado"}), 404
            
        # Verifica se o usuário tem acesso ao script
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.scripts.filter_by(id=script_id).first() is None:
            return jsonify({"error": "Você não tem permissão para editar este script"}), 403
            
        # Atualiza os campos
        script.title = data.get("title", script.title)
        script.content = data.get("content", script.content)
        script.description = data.get("description", script.description)
        
        db.session.commit()
        
        return jsonify({
            "message": "Script atualizado com sucesso",
            "script_id": script.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar script: {str(e)}"}), 500

@scripts_bp.route("/<int:script_id>", methods=["DELETE"])
@jwt_required()
def delete_script(script_id):
    """Remove um script"""
    try:
        # Busca o script
        script = Script.query.get(script_id)
        if not script:
            return jsonify({"error": "Script não encontrado"}), 404
            
        # Verifica se o usuário tem acesso ao script
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.scripts.filter_by(id=script_id).first() is None:
            return jsonify({"error": "Você não tem permissão para remover este script"}), 403
            
        # Remove a associação com o usuário
        user.scripts.remove(script)
        
        # Verifica se script ainda tem usuários associados
        if script.users.count() == 0:
            # Se não tiver mais usuários associados, remove o script do banco
            db.session.delete(script)
        
        db.session.commit()
        
        return jsonify({
            "message": "Script removido com sucesso"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao remover script: {str(e)}"}), 500

@scripts_bp.route("/<int:script_id>/share/<int:user_id>", methods=["POST"])
@jwt_required()
def share_script(script_id, user_id):
    """Compartilha um script com outro usuário"""
    try:
        # Verifica se o script existe
        script = Script.query.get(script_id)
        if not script:
            return jsonify({"error": "Script não encontrado"}), 404
            
        # Verifica se o usuário de destino existe
        target_user = User.query.get(user_id)
        if not target_user:
            return jsonify({"error": "Usuário de destino não encontrado"}), 404
            
        # Verifica se o usuário atual tem acesso ao script
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.scripts.filter_by(id=script_id).first() is None:
            return jsonify({"error": "Você não tem permissão para compartilhar este script"}), 403
            
        # Verifica se o script já está compartilhado com o usuário de destino
        if target_user.scripts.filter_by(id=script_id).first() is not None:
            return jsonify({"message": "Script já está compartilhado com este usuário"}), 200
            
        # Compartilha o script
        target_user.scripts.append(script)
        db.session.commit()
        
        return jsonify({
            "message": f"Script compartilhado com sucesso com o usuário {target_user.username}"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao compartilhar script: {str(e)}"}), 500