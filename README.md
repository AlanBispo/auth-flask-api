# Flask Auth API

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker&logoColor=white)

API RESTful para gerenciamento de usuários e autenticação, construída com Python e Flask. Este projeto serve como o back-end para o [React Auth Dashboard](https://github.com/AlanBispo/react-auth-dashboard).

## 🚀 Tecnologias

- **Framework:** Flask
- **ORM:** SQLAlchemy (MySQL)
- **Serialização:** Marshmallow
- **Autenticação:** JWT (JSON Web Tokens) com `flask-jwt-extended`
- **Infraestrutura:** Docker & Docker Compose
- **Migrations:** Flask-Migrate

## ✨ Funcionalidades

- ✅ **CRUD Completo de Usuários:** Criação, Leitura, Atualização e Deleção.
- 🔐 **Autenticação JWT:** Login seguro com geração de Access Token e Refresh Token.
- 🔄 **Silent Refresh:** Suporte para renovação silenciosa de tokens expirados.
- 🛡️ **Middleware de Segurança:** Rotas protegidas e tratamento de CORS (Cross-Origin Resource Sharing).
- 🐳 **Docker:** Ambiente de desenvolvimento pronto para uso.

## ⚙️ Como Rodar (Com Docker)

1. Clone o repositório para sua máquina.
2. Configure as Variáveis de Ambiente: Crie um arquivo .env na raiz e adicione:
   ```
       DATABASE_URL=mysql+pymysql://user:password@db:3306/flaskdb
       SECRET_KEY=sua_chave_secreta
       JWT_SECRET_KEY=sua_chave_jwt
   ```
3. Suba os containers:
   `docker compose up -d --build`

## 📍 Endpoints Principais
| Método | Rota             | Descrição                                  |
|--------|------------------|--------------------------------------------|
| POST   | `/auth/login`    | Autentica usuário e retorna tokens         |
| POST   | `/auth/refresh`  | Renova o Access Token (Requer Refresh Token)|
| GET    | `/users/`        | Lista todos os usuários (Protegido)        |
| POST   | `/users/`        | Cria um novo usuário (Público/Protegido)   |
| PUT    | `/users/{id}`    | Atualiza um usuário (Protegido)            |
| DELETE | `/users/{id}`    | Remove um usuário (Protegido)              |
