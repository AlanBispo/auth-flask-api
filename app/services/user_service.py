from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import user_schema
from werkzeug.security import generate_password_hash
from app.exceptions.custom_exceptions import EmailAlreadyExistsError, UserNotFoundError, CustomValidationError
from marshmallow import ValidationError

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, data):
        try:
            user_data = user_schema.load(data)
        except ValidationError as err:
            raise CustomValidationError(err.messages)
        
        if self.repository.find_by_email(user_data.email):
            raise EmailAlreadyExistsError()

        hashed_pw = generate_password_hash(data['password'])

        return self.repository.create(
            username=user_data.username,
            email=user_data.email,
            password=hashed_pw
        )
    
    def get_users(self):
        users = self.repository.find_all()
        return users
    
    def get_user_by_id(self, id):
        user = self.repository.find_by_id(id)
        if not user:
            raise UserNotFoundError()

        return user
    
    def update_user(self, user_id: int, data: dict):
        # busca o usuário
        user = self.repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        # se o e-mail mudou, verifica se o novo já existe
        if 'email' in data:
            existing_user = self.repository.find_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                raise EmailAlreadyExistsError()
            
        try:
            updated_data = user_schema.load(data, instance=user, partial=True)
        except ValidationError as err:
            raise CustomValidationError(err.messages)

        if 'password' in data:
            user.password = generate_password_hash(data['password'])

        return self.repository.save_update(user)
    
    def delete_user(self, user_id: int) -> dict:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
            
        self.repository.delete(user)
        
        return user_id