from flask_restful import Resource
from flask import render_template, make_response, redirect, url_for, flash
from flask_login import current_user

from src.wtform_fields import UserContactForm, AnonymContactForm


class Index(Resource):
    """
    Index Resource. Render the 'index.html' landing page.
    """
    @staticmethod
    def get():
        """ GET """
        if current_user.is_authenticated:
            return redirect(url_for('gallery'))
        return make_response(render_template('main/index.html', title="Index"), 200)


class Gallery(Resource):
    """
    Gallery Resource. Render the 'gallery.html' page depending on logged in status.
    """
    @staticmethod
    def get():
        """ GET """
        # TODO: view a random gallery of drinks
        return make_response(render_template('main/gallery.html', title="Gallery"), 200)


class Contact(Resource):
    """
    Contact Resource. Depending on method=["POST", "GET"]
    send mail or just render the 'contact.html'.
    """
    @staticmethod
    def post():
        """ POST """
        if current_user.is_authenticated:
            contact_form = UserContactForm()
        else:
            contact_form = AnonymContactForm()

        if contact_form.validate_on_submit():
            # TODO: send_mail
            flash("Your message has been sent!", "success")
            redirect(url_for('gallery'))

    @staticmethod
    def get():
        """ GET """
        if current_user.is_authenticated:
            contact_form = UserContactForm()
        else:
            contact_form = AnonymContactForm()

        if current_user.is_authenticated:
            contact_form.username_field.data = current_user.username
            contact_form.email_field.data = current_user.email

        return make_response(render_template('main/contact.html', form=contact_form, title="Contact Us"), 200)
