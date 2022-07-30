from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.oauth2 import create_access_token
from app.main import app
from app.database import Base, get_db
from app import models

SQLALCHEMY_DATABASE_URL = 'sqlite:///tests/blog-fastapi-test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {'email': 'test@demo.com', 'password': 'test'}
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user

@pytest.fixture
def test_user_2(client):
    user_data = {'email': 'user@demo.com', 'password': 'test'}
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_post(test_user, test_user_2, session):
    posts_data = [{
        'title': 'Title test one',
        'body': 'Body test one',
        'user_id': test_user['id']
    }, {
        'title': 'Title test two',
        'body': 'Body test two',
        'user_id': test_user['id']
    }, {
        'title': 'Title test one 2',
        'body': 'Body test one 2',
        'user_id': test_user_2['id']
    }, {
        'title': 'Title test two 2',
        'body': 'Body test two 2',
        'user_id': test_user_2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    
    posts_query = session.query(models.Post).all()

    return posts_query