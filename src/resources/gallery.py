from flask import render_template, make_response, redirect
from flask_restful import Resource

from src.wtform_fields import ContactForm


class Gallery(Resource):
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
        return make_response(render_template('gallery.html', form=contact_form), 200, self.headers)

    def post(self):

        # TODO:
        return redirect('/')
