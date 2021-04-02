from flask_restful import Resource
from flask import render_template

from src.wtform_fields import IndexForm


class Home(Resource):
    """
    Home Resource.
    """
    def get(self):

        index_form = IndexForm()

        return render_template('index.html', form=index_form)
