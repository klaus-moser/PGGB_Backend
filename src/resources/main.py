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
        return make_response(render_template('main/index.html'), 200)


class Gallery(Resource):
    """
    Gallery Resource.
    """
    @staticmethod
    def get():
        """
        Render the 'gallery.html' page.
        """
        if current_user.is_authenticated:
            return "Hello World"
        else:
            return "Not Hello World"


