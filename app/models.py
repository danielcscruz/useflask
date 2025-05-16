from app import db
from datetime import datetime

# Tabela de associação para relação many-to-many entre User e Script
user_scripts = db.Table('user_scripts',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('script_id', db.Integer, db.ForeignKey('scripts.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    """Modelo para usuários no sistema"""
    __tablename__ = 'users'  # Nome explícito da tabela
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relação many-to-many com Script
    scripts = db.relationship('Script', secondary=user_scripts, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return f'<User {self.username}>'

class Script(db.Model):
    """Modelo para scripts no sistema"""
    __tablename__ = 'scripts'  # Nome explícito da tabela
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Script {self.title}>'