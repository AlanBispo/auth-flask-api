class AppError(Exception):
    """Classe base para as outras exceções"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class EmailAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__("E-mail já cadastrado no sistema.", 409)

class UserNotFoundError(AppError):
    def __init__(self):
        super().__init__("Usuário não encontrado.", 404)