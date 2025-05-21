import unittest
from app.models import User, Task
from app import db
from tests.base import BaseTestCase

class TestTasks(BaseTestCase):

    def _create_and_login_user(self, username='testuser', email='test@example.com', password='password'):
        # Register user
        self.client.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=password
        ), follow_redirects=True)
        
        # Login user
        login_response = self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return login_response

    def test_create_task_requires_login(self):
        # Try to access create_task page without logging in
        response = self.client.get('/create_task', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should be redirected to login page, check for login form elements or flashed message
        self.assertIn(b'Login', response.data) # Checks for 'Login' title or button
        self.assertIn(b'Please log in to access this page.', response.data) # Default Flask-Login message

    def test_create_task(self):
        # Log in a user first
        self._create_and_login_user(username='taskmaster', email='taskmaster@example.com', password='securepassword')
        
        # Attempt to create a task
        response = self.client.post('/create_task', data=dict(
            title='My New Test Task',
            description='This is a detailed description of the test task.',
            reward=25.50
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200) # Should redirect to home or tasks list
        self.assertIn(b'Task created successfully!', response.data)
        
        # Verify task in database
        task = Task.query.filter_by(title='My New Test Task').first()
        self.assertIsNotNone(task)
        self.assertEqual(task.description, 'This is a detailed description of the test task.')
        self.assertEqual(task.reward, 25.50)
        
        # Verify task is associated with the logged-in user
        user = User.query.filter_by(email='taskmaster@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(task.employer_id, user.id)

    def test_view_tasks(self):
        # First, create a user and a task for them
        self._create_and_login_user(username='taskviewer', email='viewer@example.com', password='viewpassword')
        
        # Create a task directly or via the form post
        # For simplicity, let's post it as the user
        self.client.post('/create_task', data=dict(
            title='A Visible Task',
            description='Everyone should see this task.',
            reward=15.00
        ), follow_redirects=True)

        # Log out to ensure tasks are viewable by anyone (if that's the design)
        # Or stay logged in if tasks view is the same for auth/non-auth users
        # The current /tasks route is public.

        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A Visible Task', response.data)
        self.assertIn(b'Everyone should see this task.', response.data)
        self.assertIn(b'$15.00', response.data) # Check for formatted reward


if __name__ == '__main__':
    unittest.main()
