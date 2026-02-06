from app.models.refresh_token_model import RefreshTokenModel
from app.extensions import db

class RefreshTokenRepository:
    def create(self, token_data):
        """Salva um novo refresh token no banco"""
        new_token = RefreshTokenModel(
            token=token_data['token'],
            user_id=token_data['user_id'],
            expires_at=token_data['expires_at']
        )
        db.session.add(new_token)
        db.session.commit()
        return new_token

    def find_by_token(self, token_str):
        """Busca um token específico"""
        return RefreshTokenModel.query.filter_by(token=token_str).first()

    def delete(self, token_record):
        """Remove um token"""
        db.session.delete(token_record)
        db.session.commit()
        return True
    
    def delete_by_token(self, token_str):
        """Remove um token"""
        token = self.find_by_token(token_str)
        if token:
            db.session.delete(token)
            db.session.commit()
            return True
        return False