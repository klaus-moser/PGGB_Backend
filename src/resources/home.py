from flask_restful import Resource
from flask import render_template, make_response

from src.wtform_fields import IndexForm


class Home(Resource):
    """
    Home Resource.
    """
    def get(self):

        index_form = IndexForm()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', form=index_form), 200, headers)
