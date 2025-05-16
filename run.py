import os
from app import create_app, db
from app.models import User

app = create_app()

# Criar o banco de dados e tabelas no contexto da aplicação
@app.cli.command("init-db")
def init_db():
    """Comando para inicializar o banco de dados"""
    with app.app_context():
        db.create_all()
        print("Banco de dados inicializado!")

# Criar um usuário de teste
@app.cli.command("create-test-user")
def create_test_user():
    """Comando para criar um usuário de teste"""
    from app import bcrypt
    with app.app_context():
        if not User.query.filter_by(username="test").first():
            hashed_pw = bcrypt.generate_password_hash("password").decode('utf-8')
            user = User(username="test", password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            print("Usuário de teste criado!")
        else:
            print("Usuário de teste já existe!")

# Quando o arquivo é executado diretamente
if __name__ == "__main__":
    # Garantir que o banco de dados seja criado antes de iniciar o servidor
    with app.app_context():
        # Verificar se o diretório instance existe
        os.makedirs('instance', exist_ok=True)
        # Criar tabelas se não existirem
        db.create_all()
        print("Tabelas do banco de dados verificadas!")
    
    # Executar o servidor de desenvolvimento
    # app.run(debug=True)

    # Produção
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
