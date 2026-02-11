import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate, ma, jwt
from app.blueprints import register_blueprints
from app.hooks import register_hooks
from flask import jsonify
from app.exceptions.custom_exceptions import AppError
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {
            "ssl": {
                "fake_config": "true"
            }
        }
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    # CORS
    CORS(app, resources={r"/*": {
        "origins": ["https://react-auth-dashboard-kappa.vercel.app", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    
    register_blueprints(app)
    register_hooks(app)

    @app.errorhandler(AppError)
    def handle_custom_errors(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_errors(error):
        if isinstance(error, HTTPException):
            return jsonify({
                "error": error.name,
                "message": error.description
            }), error.code

        app.logger.error(f"Erro Crítico: {str(error)}", exc_info=True)
        response = {"error": "Erro interno no servidor"}
        if app.debug:
            response["message"] = str(error)
        return jsonify(response), 500

    return app