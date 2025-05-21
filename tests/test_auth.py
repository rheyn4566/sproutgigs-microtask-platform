import unittest
from app.models import User
from app import db
from tests.base import BaseTestCase

class TestAuth(BaseTestCase):

    def test_register_user(self):
        # Test user registration
        response = self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)
        
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_login_logout_user(self):
        # First, register a user (can be done by calling the post directly)
        self.client.post('/register', data=dict(
            username='testuser_login',
            email='testlogin@example.com',
            password='password123',
            confirm_password='password123'
        ), follow_redirects=True)

        # Test login
        login_response = self.client.post('/login', data=dict(
            email='testlogin@example.com',
            password='password123'
        ), follow_redirects=True)
        
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Login Successful!', login_response.data)
        # Check for a link that only appears when logged in (e.g., Logout or Create Task)
        self.assertIn(b'Logout', login_response.data)
        self.assertIn(b'Create Task', login_response.data)

        # Test logout
        logout_response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b'You have been logged out.', logout_response.data)
        # Check for links that appear when logged out (e.g., Login)
        self.assertIn(b'Login', logout_response.data)
        self.assertNotIn(b'Logout', logout_response.data)

if __name__ == '__main__':
    unittest.main()
