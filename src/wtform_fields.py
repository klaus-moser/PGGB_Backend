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
