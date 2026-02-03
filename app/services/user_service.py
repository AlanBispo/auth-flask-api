from app.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash
from app.exceptions.custom_exceptions import EmailAlreadyExistsError, UserNotFoundError

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, data):
        if self.repository.find_by_email(data['email']):
            raise EmailAlreadyExistsError()

        hashed_pw = generate_password_hash(data['password'])

        return self.repository.create(
            username=data['username'],
            email=data['email'],
            password=hashed_pw
        )
    
    def get_users(self):
        users = self.repository.find_all()
        return users
