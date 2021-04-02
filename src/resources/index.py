from flask_restful import Resource
from flask import render_template, make_response, redirect, url_for

from src.wtform_fields import IndexForm, ContactForm, RegisterForm


class Index(Resource):
    """
    Home Resource.
    """
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get(self):
        """
        Render the index.html page.

        :return: index.html
        """
        index_form = IndexForm()
        return make_response(render_template('index.html', form=index_form), 200, self.headers)

    def post(self):
        """
        Processes the 4 different submit-button.

        :return: Renders one of the pages /login, /register, /contact or /gallery.
        """
        # Import WTForms
        index = IndexForm()
        # login_form = LoginForm()  # TODO
        # gallery_form = GalleryForm()  # TODO

        if index.validate_on_submit():
            # Login
            if index.login_button.data:
                pass
                # return make_response(render_template('login.html', form=contact_form), 200, self.headers)

            # Register
            elif index.register_button.data:
                return redirect('/register')

            # Contact
            elif index.contact_button.data:
                return redirect('/contact')

            # View
            elif index.overview_button.data:
                pass
                # return make_response(render_template('gallery.html', form=contact_form), 200, self.headers)

        return redirect(url_for('index'))  # TODO: necessary?
