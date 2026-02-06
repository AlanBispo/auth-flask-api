import jwt
import datetime
from flask import current_app
from werkzeug.security import check_password_hash
from app.repositories.user_repository import UserRepository
from app.exceptions.custom_exceptions import UnauthorizedError

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

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

        return {
            "access_token": self.generate_token(user.id, "access"),
            "refresh_token": self.generate_token(user.id, "refresh"),
            "token_type": "Bearer"
        }

    def refresh_access_token(self, refresh_token):
        """Valida o refresh token e gera um novo access token."""
        try:
            payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            if payload.get("type") != "refresh":
                raise UnauthorizedError("Token inválido para esta operação.")

            user_id = payload['sub']
            
            new_access_token = self.generate_token(user_id, "access")
            return {"access_token": new_access_token}

        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Sessão expirada. Faça login novamente.")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Refresh token inválido.")