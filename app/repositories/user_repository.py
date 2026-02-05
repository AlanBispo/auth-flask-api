from typing import List, Optional
from app.models.user_model import UserModel
from app.extensions import db

class UserRepository:

    def create(self, username: str, email: str, password: str) -> UserModel:
        """
        Cria um novo usuário no banco de dados.

        Args:
            username (str): O nome de usuário escolhido.
            email (str): O endereço de e-mail único do usuário.
            password (str): A senha já criptografada (hash).

        Returns:
            UserModel: A instância do usuário recém-criada com o ID gerado pelo banco.
        """
        user = UserModel(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def find_by_email(self, email: str) -> Optional[UserModel]:
        """
        Busca um usuário através do endereço de e-mail.

        Args:
            email (str): O e-mail para pesquisa.

        Returns:
            Optional[UserModel]: O objeto usuário se encontrado, caso contrário, None.
        """
        return UserModel.query.filter_by(email=email).first()

    def find_all(self) -> List[UserModel]:
        """
        Recupera todos os usuários cadastrados no sistema.

        Returns:
            List[UserModel]: Uma lista contendo todos os objetos de usuários.
        """
        return UserModel.query.all()

    def find_by_id(self, id: int) -> Optional[UserModel]:
        """
        Busca um usuário específico através do seu ID (Chave Primária).

        Args:
            id (int): O identificador único do usuário.

        Returns:
            Optional[UserModel]: O objeto usuário se encontrado, caso contrário, None.
        """
        return UserModel.query.filter_by(id=id).first()
    
    def save_update(self, user: UserModel) -> UserModel:
        """Salva alterações em um objeto já existente."""
        db.session.add(user)
        db.session.commit()
        return user
    
    def delete(self, user: UserModel) -> None:
        """ Remove um usuário do banco de dados. """
        db.session.delete(user)
        db.session.commit()