from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    # Relationship to tasks
    tasks = db.relationship('Task', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

    @staticmethod
    def get_default_categories():
        """Returns a list of default category names for seeding the database."""
        return [
            ('Data Entry', 'Tasks involving data input and management'),
            ('Writing', 'Content writing, copywriting, and editing tasks'),
            ('Research', 'Research and data collection tasks'),
            ('Design', 'Graphic design and creative tasks'),
            ('Survey', 'Survey completion and feedback tasks'),
            ('Testing', 'Software testing and quality assurance tasks'),
            ('Social Media', 'Social media management and engagement tasks'),
            ('Translation', 'Language translation and localization tasks'),
            ('Other', 'Miscellaneous tasks that do not fit other categories'),
        ]


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reward = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    # Optional: define relationship to User (Employer)
    # employer = db.relationship('User', backref=db.backref('tasks_posted', lazy=True))

    def __repr__(self):
        return f'<Task {self.title}>'
