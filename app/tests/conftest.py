import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    """Cria e configura uma nova instância do app para cada teste."""
    app = create_app()
    
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # usando sqlite
        "JWT_SECRET_KEY": "test_secret", 
    })
    # cria o banco
    with app.app_context():
        db.create_all()
        yield app
        # remove após finalizar
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()