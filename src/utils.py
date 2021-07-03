from re import fullmatch
from flask import current_app
from flask_mail import Message
from create_app import mail


class Utils:
    """
    Class with useful functions
    """

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate a given email for its format: {String}+@{String}.{String}

        :param email: Email to be validated by RegEx.
        """

        regex = '^[^@]+@{1}[^@]+[.]{1}[^@]+$'

        if not fullmatch(regex, email):
            return False
        return True

    # TODO: https://github.com/miguelgrinberg/flasky/blob/master/app/email.py


class FlaskMail:

    @staticmethod
    def send_email(subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body

        mail.send(msg)

    # TODO:
