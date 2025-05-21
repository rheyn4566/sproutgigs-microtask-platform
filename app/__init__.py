from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Route function name for the login page
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular dependency
        return User.query.get(int(user_id))

    with app.app_context():
        from . import routes  # Import routes
        # Import models here to ensure they are registered with SQLAlchemy
        # User model is already imported by routes or will be by db.create_all implicitly
        # No, it needs to be explicit if load_user is to work reliably before first request potentially.
        # The models need to be known to SQLAlchemy before create_all.
        # The original structure had `from .models import User` here, which is good.
        from .models import User, Task # Ensure Task model is imported
        db.create_all()  # Create database tables

    return app
