from flask import render_template, make_response, redirect, url_for, flash, Blueprint, request
from flask_login import current_user

from src.wtform_fields import UserContactForm, AnonymContactForm


main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def index():
    """
    Index Resource. Render the 'index.html' landing page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.gallery'))
    return make_response(render_template('main/index.html', title="Index"), 200)


@main.route('/gallery', methods=["GET"])  # TODO: gallery/<view>
def gallery():
    """
    Gallery Resource. Render the 'gallery.html' page depending on logged in status.
    """
    # TODO: view a random gallery of drinks
    return make_response(render_template('main/gallery.html', title="Gallery"), 200)


@main.route('/contact', methods=["GET", "POST"])
def contact():
    """
    Contact Resource. Depending on method=["POST", "GET"]
    send mail or just render the 'contact.html'.
    """
    if current_user.is_authenticated:
        contact_form = UserContactForm()
    else:
        contact_form = AnonymContactForm()

    if contact_form.validate_on_submit():
        # TODO: send_mail
        flash("Your message has been sent!", "success")
        redirect(url_for('main.gallery'))

    elif request.method == 'GET':

        if current_user.is_authenticated:
            contact_form.username_field.data = current_user.username
            contact_form.email_field.data = current_user.email
        return make_response(render_template('main/contact.html', form=contact_form, title="Contact Us"), 200)
