from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Inicialização das extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões com o app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importar rotas aqui para evitar importações circulares
    from app.routes import auth_bp
    from app.scripts import scripts_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(scripts_bp, url_prefix='/api/scripts')

    # Garantir que as pastas necessárias existam
    import os
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    os.makedirs(os.path.join(instance_path, 'instance'), exist_ok=True)

    return app