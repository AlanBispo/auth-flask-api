def test_register_user(client):
    """Teste: registrar um usuário novo."""

    # cria usuário
    response = client.post("/users/", json={
        "username": "tester",
        "email": "test@email.com",
        "password": "teste123"
    })
    
    assert response.status_code == 201
    assert response.json["username"] == "tester"

def test_login_user(client):
    """Teste: fluxo de registro seguido de login."""
    # cria usuário
    client.post("/users/", json={
        "username": "tester",
        "email": "test@email.com",
        "password": "teste123"
    })

    # login
    response = client.post("/auth/login", json={
        "email": "test@email.com",
        "password": "teste123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json

def test_access_protected_route(client):
    """Teste: funcionamento do tokem em rota protegida."""
    # cria usuário
    register_resp = client.post("/users/", json={ 
        "username": "tester_token",
        "email": "teste_token@email.com", 
        "password": "teste123" 
    })
    assert register_resp.status_code == 201

    # faz login
    login_resp = client.post("/auth/login", json={ 
        "email": "teste_token@email.com", 
        "password": "teste123" 
    })
    assert login_resp.status_code == 200
    token = login_resp.json["access_token"]

    # tenta acessar rota protegida sem token -> falha
    resp_fail = client.get("/users/")
    assert resp_fail.status_code == 401

    # tenta acessar rota protegida com token -> sucesso
    resp_ok = client.get("/users/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp_ok.status_code == 200
    assert isinstance(resp_ok.json, list)