# API Flask com Autenticação JWT

Este projeto implementa uma API em Flask com autenticação JWT, utilizando SQLAlchemy como ORM para persistência de dados.

## Estrutura do Projeto

```
app/
├── __init__.py    # Inicialização da aplicação e registro dos blueprints
├── models.py      # Modelos User e Script com relação many-to-many
├── routes.py      # Define o blueprint de autenticação (auth_bp)
├── auth.py        # Funções de autenticação (register, login, protected)
├── scripts.py     # Define o blueprint de scripts (scripts_bp) e suas funções
config.py          # Configurações da aplicação
run.py             # Script para executar a aplicação
instance/          # Pasta onde o banco de dados será criado
└── app.db
```

## Organização dos Blueprints

O projeto está organizado em blueprints para melhor modularidade:

1. **auth_bp**: Gerencia autenticação (registrar, login)
   - Prefixo de URL: `/api`
   - Definido em: `routes.py`
   - Implementação em: `auth.py`

2. **scripts_bp**: Gerencia operações com scripts
   - Prefixo de URL: `/api/scripts`
   - Definido e implementado em: `scripts.py`

Ambos os blueprints são registrados no aplicativo Flask no arquivo `__init__.py`.

## Requisitos

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-JWT-Extended
- python-dotenv

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instale as dependências:
   ```
   pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended python-dotenv
   ```

## Configuração

Você pode criar um arquivo `.env` na raiz do projeto para definir variáveis de ambiente:

```
SECRET_KEY=seu_secret_key_seguro
JWT_SECRET_KEY=seu_jwt_secret_key_seguro
DATABASE_URL=sqlite:///instance/app.db
```

## Executando a Aplicação

1. Inicialize o banco de dados:
   ```
   flask --app run.py init-db
   ```

2. (Opcional) Crie um usuário de teste:
   ```
   flask --app run.py create-test-user
   ```

3. Execute a aplicação:
   ```
   python run.py
   ```

A API estará disponível em `http://localhost:5000/api/`

## Endpoints da API

### Autenticação

- `GET /api/` - Verificar se a API está funcionando
- `POST /api/register` - Registrar novo usuário
  ```json
  {
    "username": "seu_usuario",
    "password": "sua_senha"
  }
  ```
- `POST /api/login` - Fazer login e obter token JWT
  ```json
  {
    "username": "seu_usuario",
    "password": "sua_senha"
  }
  ```
- `GET /api/protected` - Endpoint protegido (requer token JWT)
  - Header: `Authorization: Bearer seu_token_jwt`

### Scripts

Todos os endpoints de scripts requerem autenticação JWT (Header: `Authorization: Bearer seu_token_jwt`)

- `GET /api/scripts/` - Obter todos os scripts do usuário atual
- `GET /api/scripts/all` - Obter todos os scripts do sistema
- `GET /api/scripts/<script_id>` - Obter detalhes de um script específico
- `POST /api/scripts/` - Criar um novo script
  ```json
  {
    "title": "Título do Script",
    "content": "Conteúdo do Script",
    "description": "Descrição opcional"
  }
  ```
- `PUT /api/scripts/<script_id>` - Atualizar um script existente
  ```json
  {
    "title": "Novo Título",
    "content": "Novo Conteúdo",
    "description": "Nova Descrição"
  }
  ```
- `DELETE /api/scripts/<script_id>` - Remover um script
- `POST /api/scripts/<script_id>/share/<user_id>` - Compartilhar um script com outro usuário

## Modelos de Dados

### User (Usuário)
- id: ID único do usuário
- username: Nome de usuário único
- password: Senha criptografada
- created_at: Data de criação do usuário
- scripts: Lista de scripts associados ao usuário

### Script
- id: ID único do script
- title: Título do script
- content: Conteúdo do script
- description: Descrição opcional
- created_at: Data de criação
- updated_at: Data da última atualização
- users: Lista de usuários associados ao script

## Solução de Problemas

- Se o banco de dados não for criado automaticamente:
  - Certifique-se de que o diretório `instance` existe na raiz do projeto
  - Execute o comando `flask --app run.py init-db` para inicializar manualmente o banco de dados
  
- Para verificar se o banco de dados foi criado corretamente:
  - Após iniciar a aplicação, verifique se o arquivo `instance/app.db` foi criado na raiz do projeto

- Se ocorrerem erros de importação:
  - Certifique-se de que a estrutura do projeto está correta
  - Verifique se está executando os comandos a partir da raiz do projeto
