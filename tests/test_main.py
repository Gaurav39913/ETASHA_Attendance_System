import unittest
from app import create_app, db
from app.auth.models import User

class MainRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        user = User(login_id='testuser', name='Test User', email='test@example.com', password='password', center='Test Center', is_admin=False)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

if __name__ == '__main__':
    unittest.main()