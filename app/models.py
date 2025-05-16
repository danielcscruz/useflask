from app import db
from datetime import datetime

class User(db.Model):
    """Modelo para usuários no sistema"""
    __tablename__ = 'users'  # Nome explícito da tabela
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'