from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
    # TODO: check existing email (registered user)
    # TODO: check email format
    email_field = StringField('email_field', validators=[
        InputRequired(message='Email required!'),
        Length(min=4, max=25, message='Put in a valid E-Mail adress!')])

    text_field = StringField('text_field', validators=[
        InputRequired(message='Message'),
        Length(min=4, max=25, message='Message cannot be empty!')])

    send_button = SubmitField('Send')
