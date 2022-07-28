from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = 'sqlite:///tests/blog-fastapi-test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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