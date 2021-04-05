from flask_wtf import FlaskForm
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from src.models.user import UserModel


class AnonymContactForm(FlaskForm):
    """
    This is the base form class for the '/contact' endpoint.
    """
    email_field = StringField('email_field', validators=[
        InputRequired(message='Email'),
        Length(min=4, max=25, message='Put in a valid E-Mail address!')])

    text_field = TextAreaField('text_field', validators=[
        InputRequired(message='Message'),
        Length(min=1, max=200, message='Message cannot be empty!')])

    send_button = SubmitField('Send')

    # TODO: check email format (Regex)
    def check_email_format(self):
        ...


class UserContactForm(AnonymContactForm):
    """
    Contact form for logged in users.
    """
    username_field = StringField('username_field', validators=[
        InputRequired()])


class RegisterForm(FlaskForm):
    """
    This is the form class for the '/register' endpoint.
    """
    username = StringField('username_label', validators=[
        InputRequired(message='Username required!'),
        Length(min=4, max=25, message='Username must be between 4-25 characters!')])

    email = StringField('email_label', validators=[
        InputRequired(message='Email required!'),
        Length(min=4, max=80, message='Must be a valid Email!')])

    password = PasswordField('password_label', validators=[
        InputRequired(message='Password required!'),
        Length(min=6, max=30, message='Password must be between 4-25 characters!')])

    confirm_pwd = PasswordField('confirm_pwd_label', validators=[
        InputRequired(message='Password required!'),
        EqualTo('password', message='Passwords must match!')])

    submit_button = SubmitField('Register')

    # Custom validator to check username upfront
    def validate_username(self, username) -> None:
        """
        Validate a given username.
        :param username: Username to be validated via the database.
        """
        if UserModel.find_by_username(username=username.data):
            raise ValidationError("A user '{}' already exists!".format(username.data))


class LoginForm(FlaskForm):
    """
    This is the form class for the '/login' endpoint.
    """
    def validate_credentials(self, field: PasswordField) -> None:
        """
        Check the credentials from the LoginForm.
        """
        username_entered = self.username.data
        password_entered = field.data

        user = UserModel.find_by_username(username=username_entered)

        # Check if credentials are valid
        if user is None:
            raise ValidationError("Username or password is incorrect!")
        elif not pbkdf2_sha256.verify(password_entered, user.password):
            raise ValidationError("Username or password is incorrect!")

    username = StringField('username_label', validators=[
        InputRequired(message='Username required!')])

    password = PasswordField('password_label', validators=[
        InputRequired(message='Password required!'), validate_credentials])

    login_button = SubmitField('Login')
