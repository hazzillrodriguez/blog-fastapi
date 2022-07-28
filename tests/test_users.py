import pytest
from app import schemas
from app.config import settings

from jose import jwt

def test_create_user(client):
    res = client.post('/users/', json={'email': 'test@demo.com', 'password': 'test'})
    new_user = schemas.UserResponse(**res.json())
    
    assert res.status_code == 201
    assert new_user.email == 'test@demo.com'

def test_login_success(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = payload.get('user_id')
    
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('email, password, status', [
    ('wrong@email.com', 'test', 403),
    ('test@demo.com', 'wrong-password', 403),
    (None, 'test', 422),
    ('test@demo.com', None, 422),
])
def test_login_failed(client, test_user, email, password, status):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status