from flask import render_template, url_for, flash, redirect, current_app, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Task, Category
from app.forms import RegistrationForm, LoginForm, TaskForm, TaskFilterForm
from werkzeug.security import generate_password_hash, check_password_hash

# When routes.py is imported within create_app's app_context,
# current_app points to the application instance.
# So, current_app.route can be used to define routes.


def seed_categories():
    """Seed the database with default categories if they don't exist."""
    if Category.query.count() == 0:
        for name, description in Category.get_default_categories():
            category = Category(name=name, description=description)
            db.session.add(category)
        db.session.commit()


def get_category_choices(include_all=False):
    """Get category choices for select fields."""
    categories = Category.query.order_by(Category.name).all()
    choices = [(c.id, c.name) for c in categories]
    if include_all:
        choices.insert(0, (0, 'All Categories'))
    return choices


@current_app.route('/')
@current_app.route('/home')
def home():
    return "Home Page Placeholder"


@current_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)


@current_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@current_app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@current_app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    # Ensure categories exist
    seed_categories()
    
    form = TaskForm()
    form.category.choices = [(0, 'Select a category...')] + get_category_choices()
    
    if form.validate_on_submit():
        category_id = form.category.data if form.category.data != 0 else None
        task = Task(title=form.title.data,
                    description=form.description.data,
                    reward=form.reward.data,
                    employer_id=current_user.id,
                    category_id=category_id)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('create_task.html', title='Create Task', form=form)


@current_app.route('/tasks')
def tasks():
    # Ensure categories exist
    seed_categories()
    
    # Get filter form
    filter_form = TaskFilterForm()
    filter_form.category.choices = get_category_choices(include_all=True)
    
    # Get category filter from query params
    category_id = request.args.get('category', 0, type=int)
    filter_form.category.data = category_id
    
    # Build query with optional category filter
    query = Task.query
    if category_id > 0:
        query = query.filter_by(category_id=category_id)
    
    all_tasks = query.order_by(Task.created_at.desc()).all()
    
    # Get all categories for display
    categories = Category.query.order_by(Category.name).all()
    
    return render_template('tasks.html',
                          title='Available Tasks',
                          tasks=all_tasks,
                          filter_form=filter_form,
                          categories=categories,
                          selected_category=category_id)


@current_app.route('/categories')
def list_categories():
    """List all available task categories."""
    seed_categories()
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories.html', title='Task Categories', categories=categories)
