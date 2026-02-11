from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity
)
from app.services.auth_service import AuthService

auth_bp =   Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validação simples de entrada
    if not data or 'email' not in data or 'password' not in data: 
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

    result = auth_service.login(data['email'], data['password'])
    
    return jsonify(result), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify(access_token=new_access_token), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao renovar token, {e}"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    
    if not data or 'refresh_token' not in data:
        return jsonify({"error": "O refresh_token é obrigatório para o logout."}), 400

    result = auth_service.logout(data['refresh_token'])
    
    return jsonify(result), 200