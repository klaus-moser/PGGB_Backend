from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

from src.wtform_fields import UploadMemeForm
from src.models.meme import MemeModel


meme = Blueprint('meme', __name__)


@meme.route('/meme_page')
def meme_page():
    ...
    # TODO:
    return "Hello world"


@meme.route('/upload', methods=["POST", "GET"])
def upload():
    """
    Upload a new meme.
    """
    upload_form = UploadMemeForm()

    if upload_form.validate_on_submit():
        meme_ = MemeModel(upload_form.meme_name_label.data, current_user.id)
        meme_.save_to_db()
        return redirect(url_for('main.gallery'))

    return render_template('meme/upload.html', form=upload_form)
