import jwt
from flask import request, jsonify, current_app, g
from app.models.user_model import UserModel

def register_hooks(app):
    
    @app.before_request
    def check_authentication():
        public_endpoints = ['auth.login', 'user.create_user', 'static']

        if not request.endpoint or request.endpoint in public_endpoints:
            return

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token ausente ou malformado. Use o padrão Bearer."}), 401

        token = auth_header.split(" ")[1]

        try:
            # decodifica o token
            payload = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=["HS256"]
            )

            # Validação de tipo
            if payload.get("type") != "access":
                print("DEBUG: Erro - Tentativa de usar Refresh Token como Access")
                return jsonify({"error": "Token inválido para esta operação."}), 403

            user = UserModel.query.get(payload['sub'])
            if not user:
                print(f"DEBUG: Usuário ID {payload['sub']} não encontrado no banco")
                return jsonify({"error": "Usuário não encontrado."}), 401

            g.user = user

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Sessão expirada. Faça login novamente."}), 401
        
        except jwt.InvalidTokenError as e:
            return jsonify({"error": "Token inválido."}), 401
            
        except Exception as e:
            app.logger.error(f"Erro crítico: {str(e)}")
            return jsonify({"error": "Erro interno de autenticação."}), 500