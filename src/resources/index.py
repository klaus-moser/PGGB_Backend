from flask_restful import Resource
from flask import render_template, make_response, redirect, url_for
from flask_login import current_user

from src.wtform_fields import IndexForm


class Index(Resource):
    """
    Home Resource.
    """
    @staticmethod
    def get():
        """
        Render the index.html landing page.
        """
        if current_user.is_authenticated:
            return "Hello World"
            # return redirect(url_for('gallery'))

        index_form = IndexForm()
        return make_response(render_template('index.html', form=index_form), 200)

    @staticmethod
    def post():
        """
        Processes the 4 different submit-button.

        :return: Renders one of the pages /login, /register, /contact or /gallery.
        """
        index = IndexForm()

        if index.validate_on_submit():

            if index.login_button.data:
                return redirect('/login')

            elif index.register_button.data:
                return redirect('/register')

            elif index.contact_button.data:
                return redirect('/contact')

            elif index.overview_button.data:
                return redirect('/gallery')

        return redirect(url_for('index'))  # TODO: necessary?
