import jwt
import datetime
from flask import current_app
from werkzeug.security import check_password_hash
from app.repositories.user_repository import UserRepository
from app.exceptions.custom_exceptions import UnauthorizedError
from app.models.refresh_token_model import RefreshTokenModel
from app.extensions import db
from app.repositories.refresh_token_repository import RefreshTokenRepository

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.token_repository = RefreshTokenRepository()

    def generate_token(self, user_id, token_type="access"):
        """
        Gera um JWT.
        token_type: "access" ou "refresh"
        """
        if token_type == "access":
            days, minutes = 0, 30  # Access token dura 30 min
        else:
            days, minutes = 7, 0   # Refresh token dura 7 dias

        payload = {
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=days, minutes=minutes),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "sub": str(user_id),
            "type": token_type
        }
        
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    def login(self, email, password):
        user = self.user_repository.find_by_email(email)
        if not user or not check_password_hash(user.password, password):
            raise UnauthorizedError()

        access_token = self.generate_token(user.id, "access")
        refresh_token_str = self.generate_token(user.id, "refresh")

        self.token_repository.create({
            "token": refresh_token_str,
            "user_id": user.id,
            "expires_at": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        })

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str
        }

    def refresh_access_token(self, refresh_token_str):
        token_record = self.token_repository.find_by_token(refresh_token_str)
    
        if not token_record:
            raise UnauthorizedError("Sessão inválida.")

        try:
            payload = jwt.decode(refresh_token_str, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            if payload.get("type") != "refresh":
                raise UnauthorizedError("Tipo de token inválido.")

            # novo Access Token
            new_access = self.generate_token(payload['sub'], "access")
            return {"access_token": new_access}

        except jwt.ExpiredSignatureError:
            # limpa o banco
            self.token_repository.delete(token_record)
            raise UnauthorizedError("Sessão expirada. Faça login novamente.")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Token corrompido.")
        
    def logout(self, refresh_token):
        """
        Revoga o acesso do usuário removendo o refresh token do banco.
        """
        result = self.token_repository.delete_by_token(refresh_token)
        
        if not result:
            raise UnauthorizedError("Sessão já é inválida ou o token não existe.")
            
        return {"message": "Logout realizado com sucesso."}