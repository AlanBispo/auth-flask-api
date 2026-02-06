from app.blueprints.user_routes import user_bp
from app.blueprints.auth_routes import auth_bp

def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')