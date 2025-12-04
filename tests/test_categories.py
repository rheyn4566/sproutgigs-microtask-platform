import unittest
from app.models import User, Task, Category
from app import db
from tests.base import BaseTestCase


class TestCategories(BaseTestCase):

    def _create_and_login_user(self, username='testuser', email='test@example.com', password='password'):
        """Helper method to register and login a user."""
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

    def test_category_model_creation(self):
        """Test that a Category can be created and saved to the database."""
        category = Category(name='Test Category', description='A test category')
        db.session.add(category)
        db.session.commit()
        
        retrieved = Category.query.filter_by(name='Test Category').first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, 'Test Category')
        self.assertEqual(retrieved.description, 'A test category')

    def test_category_unique_name(self):
        """Test that category names must be unique."""
        category1 = Category(name='Unique Category', description='First')
        db.session.add(category1)
        db.session.commit()
        
        category2 = Category(name='Unique Category', description='Second')
        db.session.add(category2)
        
        with self.assertRaises(Exception):
            db.session.commit()

    def test_default_categories(self):
        """Test that default categories are properly defined."""
        defaults = Category.get_default_categories()
        self.assertIsInstance(defaults, list)
        self.assertGreater(len(defaults), 0)
        
        # Each default should be a tuple of (name, description)
        for item in defaults:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)

    def test_task_category_relationship(self):
        """Test that a Task can be associated with a Category."""
        # Create a user first
        user = User(username='employer', email='employer@test.com', password_hash='hash')
        db.session.add(user)
        db.session.commit()
        
        # Create a category
        category = Category(name='Writing', description='Writing tasks')
        db.session.add(category)
        db.session.commit()
        
        # Create a task with the category
        task = Task(
            title='Write an Article',
            description='Write a 500 word article',
            reward=10.00,
            employer_id=user.id,
            category_id=category.id
        )
        db.session.add(task)
        db.session.commit()
        
        # Verify the relationship
        retrieved_task = Task.query.filter_by(title='Write an Article').first()
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.category_id, category.id)
        self.assertEqual(retrieved_task.category.name, 'Writing')
        
        # Verify reverse relationship
        self.assertIn(task, category.tasks)

    def test_task_without_category(self):
        """Test that a Task can exist without a category (nullable)."""
        user = User(username='employer2', email='employer2@test.com', password_hash='hash')
        db.session.add(user)
        db.session.commit()
        
        task = Task(
            title='No Category Task',
            description='This task has no category',
            reward=5.00,
            employer_id=user.id,
            category_id=None
        )
        db.session.add(task)
        db.session.commit()
        
        retrieved = Task.query.filter_by(title='No Category Task').first()
        self.assertIsNotNone(retrieved)
        self.assertIsNone(retrieved.category_id)
        self.assertIsNone(retrieved.category)

    def test_categories_page(self):
        """Test that the categories page loads correctly."""
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Categories', response.data)

    def test_categories_seeded_on_page_load(self):
        """Test that categories are seeded when accessing the categories page."""
        # Initially no categories
        self.assertEqual(Category.query.count(), 0)
        
        # Access categories page
        self.client.get('/categories')
        
        # Categories should now be seeded
        self.assertGreater(Category.query.count(), 0)

    def test_tasks_page_with_filter(self):
        """Test that tasks can be filtered by category."""
        # Create user and login
        self._create_and_login_user(username='filterer', email='filter@test.com', password='filterpass')
        
        # Access tasks page to seed categories
        self.client.get('/tasks')
        
        # Get a category
        category = Category.query.first()
        self.assertIsNotNone(category)
        
        # Create a task with this category
        self.client.post('/create_task', data=dict(
            title='Categorized Task Test',
            description='This task has a category for filtering',
            reward=20.00,
            category=category.id
        ), follow_redirects=True)
        
        # Test filter by category
        response = self.client.get(f'/tasks?category={category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Categorized Task Test', response.data)

    def test_tasks_page_filter_all(self):
        """Test that filtering with category=0 shows all tasks."""
        response = self.client.get('/tasks?category=0')
        self.assertEqual(response.status_code, 200)

    def test_create_task_with_category(self):
        """Test creating a task with a category selected."""
        self._create_and_login_user(username='creator', email='creator@test.com', password='createpass')
        
        # Access create_task to seed categories
        self.client.get('/create_task')
        
        # Get a category
        category = Category.query.first()
        self.assertIsNotNone(category)
        
        # Create task with category
        response = self.client.post('/create_task', data=dict(
            title='Task With Category',
            description='This task should have a category assigned',
            reward=15.00,
            category=category.id
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task created successfully!', response.data)
        
        # Verify task has category
        task = Task.query.filter_by(title='Task With Category').first()
        self.assertIsNotNone(task)
        self.assertEqual(task.category_id, category.id)

    def test_create_task_without_category(self):
        """Test creating a task without selecting a category."""
        self._create_and_login_user(username='nocatcreator', email='nocat@test.com', password='nocatpass')
        
        # Access create_task to seed categories
        self.client.get('/create_task')
        
        # Create task without category (category=0 means no selection)
        response = self.client.post('/create_task', data=dict(
            title='Task Without Category',
            description='This task should have no category',
            reward=10.00,
            category=0
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task created successfully!', response.data)
        
        # Verify task has no category
        task = Task.query.filter_by(title='Task Without Category').first()
        self.assertIsNotNone(task)
        self.assertIsNone(task.category_id)

    def test_category_badge_displayed(self):
        """Test that category badge is displayed for tasks with categories."""
        self._create_and_login_user(username='badgetest', email='badge@test.com', password='badgepass')
        
        # Access create_task to seed categories
        self.client.get('/create_task')
        
        # Get a category
        category = Category.query.first()
        
        # Create task with category
        self.client.post('/create_task', data=dict(
            title='Badge Test Task',
            description='Testing category badge display',
            reward=25.00,
            category=category.id
        ), follow_redirects=True)
        
        # Check tasks page shows the category
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(category.name.encode(), response.data)


if __name__ == '__main__':
    unittest.main()
