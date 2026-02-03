import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate, ma
from app.blueprints import register_blueprints
from flask import jsonify
from app.exceptions.custom_exceptions import AppError

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    register_blueprints(app)

    @app.errorhandler(AppError)
    def handle_custom_errors(error):
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    def handle_generic_errors(error):
        return jsonify({"error": "Erro interno no servidor",}), 500

    return app