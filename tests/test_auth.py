from app import create_app, db
from app.auth.models import User
import pytest

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    assert response.status_code == 302  # Redirect after successful registration
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.name == 'Test User'

def test_login(client):
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 302  # Redirect after successful login
    assert 'user_id' in client.session  # Check if user_id is in session

def test_logout(client):
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect after logout
    assert 'user_id' not in client.session  # Check if user_id is removed from session

def test_password_hashing():
    user = User(name='Test User', email='test@example.com', password='password')
    assert user.check_password('password') is True
    assert user.check_password('wrong_password') is False