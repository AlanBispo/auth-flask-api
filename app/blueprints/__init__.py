from app.blueprints.user_routes import user_bp
from app.blueprints.auth_routes import auth_bp

def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix='/users', strict_slashes=False)
    app.register_blueprint(auth_bp, url_prefix='/auth', strict_slashes=False)