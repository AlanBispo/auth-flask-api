import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def hello_world():
        return {"message": "Hello World! Funcionando..."}, 200

    return app