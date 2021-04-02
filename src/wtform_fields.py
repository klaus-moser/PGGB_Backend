from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from src.models.user import UserModel


class IndexForm(FlaskForm):
    """
    This is the form class for the index.html.
    """
    login_button = SubmitField('Login')
    register_button = SubmitField('Register')
    overview_button = SubmitField('Have a look!')
    contact_button = SubmitField('Contact us?')


class ContactForm(FlaskForm):
    """
    This is the form class for the '/contact' endpoint.
    """
    email_field = StringField('email_field', validators=[
        InputRequired(message='Email required!'),
        Length(min=4, max=25, message='Put in a valid E-Mail address!')])

    text_field = TextAreaField('text_field', validators=[
        InputRequired(message='Message'),
        Length(min=1, max=200, message='Message cannot be empty!')])

    send_button = SubmitField('Send')

    # TODO: check email format (Regex)
    def check_email_format(self):
        ...


class RegisterForm(FlaskForm):
    """
    This is the form class for the '/register' endpoint.
    """
    username = StringField('username_label', validators=[
        InputRequired(message='Username required!'),
        Length(min=4, max=25, message='Username must be between 4-25 characters!')])

    email = StringField('email_label', validators=[
        InputRequired(message='Email required!'),
        Length(min=4, max=25, message='Must be a valid Email!')])

    password = PasswordField('password_label', validators=[
        InputRequired(message='Password required!'),
        Length(min=4, max=25, message='Password must be between 4-25 characters!')])

    confirm_pwd = PasswordField('confirm_pwd_label', validators=[
        InputRequired(message='Password required!'),
        EqualTo('password', message='Passwords must match!')])

    submit_button = SubmitField('Register')
    # TODO: check username
    # # Custom validator to check username upfront
    # def validate_username(self, username) -> None:
    #     """
    #     Validate a given username.
    #
    #     :param username: Username to be validated via the database.
    #     :return: None.
    #     """
    #     if UserModel.find_by_username(username=username.data):
    #         raise ValidationError("A user '{}' already exists!".format(username.data))
    #