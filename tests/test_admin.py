import pytest
from app import create_app, db
from app.auth.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    user = User(login_id='admin', name='Admin User', email='admin@example.com', password='password', is_admin=True)
    db.session.add(user)
    db.session.commit()

def test_admin_dashboard(client, init_database):
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Admin User' in response.data

def test_user_management(client, init_database):
    response = client.get('/admin/manage_users')
    assert response.status_code == 200
    assert b'User Management' in response.data

def test_admin_access(client):
    response = client.get('/admin/dashboard')
    assert response.status_code == 200

def test_non_admin_access(client):
    user = User(login_id='user', name='Regular User', email='user@example.com', password='password', is_admin=False)
    db.session.add(user)
    db.session.commit()
    
    with client:
        client.post('/login', data={'email': 'user@example.com', 'password': 'password'})
        response = client.get('/admin/dashboard')
        assert response.status_code == 403  # Forbidden access for non-admin users