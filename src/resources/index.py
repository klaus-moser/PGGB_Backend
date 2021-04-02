from flask_restful import Resource
from flask import render_template, make_response, redirect, url_for

from src.wtform_fields import IndexForm


class Index(Resource):
    """
    Home Resource.
    """
    def get(self) -> tuple:
        """
        Index page.

        :return: index.html
        """
        index_form = IndexForm()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', form=index_form), 200, headers)

    def post(self):

        return redirect(url_for('login'))
