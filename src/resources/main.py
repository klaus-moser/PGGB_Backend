from flask_restful import Resource
from flask import render_template, make_response, redirect, url_for
from flask_login import current_user


class Index(Resource):
    """
    Index Resource.
    """
    @staticmethod
    def get():
        """
        Render the 'index.html' landing page.
        """
        if current_user.is_authenticated:
            return redirect(url_for('gallery'))
        return make_response(render_template('main/index.html', title="Index"), 200)


class Gallery(Resource):
    """
    Gallery Resource.
    """
    @staticmethod
    def get():
        """
        Render the 'gallery.html' page.
        """
        return make_response(render_template('main/gallery.html', title="Gallery"), 200)


class Contact(Resource):
    """
    Contact Resource.
    """
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get(self):
        """
        Render the 'contact.html'.

        :return: 'contact.html'
        """
        contact_form = ContactForm()
        return make_response(render_template('main/contact.html', form=contact_form), 200, self.headers)

    def post(self):
        """
        Takes the post request to send the E-mail.
        Pop-Up to inform the user.

        :return: '/'
        """
        # TODO: send email
        # TODO: Info-pop up
        return redirect('/')
