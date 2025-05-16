import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env se existir
load_dotenv()

# Define o caminho base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configurações gerais
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    
    # Configurações do SQLAlchemy
    # Usa um caminho absoluto para o banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações do JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')