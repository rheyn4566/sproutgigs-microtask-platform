from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    reward = FloatField('Reward', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Create Task')


class TaskFilterForm(FlaskForm):
    """Form for filtering tasks by category."""
    category = SelectField('Filter by Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Filter')
