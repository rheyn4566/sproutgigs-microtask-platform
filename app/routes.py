from flask import render_template, url_for, flash, redirect, current_app, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Task # Import Task model
from app.forms import RegistrationForm, LoginForm, TaskForm # Import TaskForm
from werkzeug.security import generate_password_hash, check_password_hash

# When routes.py is imported within create_app's app_context,
# current_app points to the application instance.
# So, current_app.route can be used to define routes.

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
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,
                    reward=form.reward.data,
                    employer_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('home')) # Or a future 'task_detail' or 'dashboard' page
    return render_template('create_task.html', title='Create Task', form=form)

@current_app.route('/tasks')
def tasks():
    all_tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', title='Available Tasks', tasks=all_tasks)
