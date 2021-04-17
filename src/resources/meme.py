from cloudinary.exceptions import Error
from string import ascii_letters, digits
from random import choice
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from werkzeug.utils import secure_filename
from uuid import uuid4
from pathlib import Path

from src.wtform_fields import UploadMemeForm
from src.models.meme import MemeModel


meme = Blueprint('meme', __name__)


@meme.route('/meme_page', methods=["GET"])
def meme_page():
    ...
    # TODO:
    return render_template('meme/meme.html')


@meme.route('/upload', methods=["POST", "GET"])
def upload():
    """
    Upload a new meme.
    """
    upload_form = UploadMemeForm()

    if upload_form.validate_on_submit():

        # Secure filename
        file = upload_form.img_url.data.filename
        file_name = secure_filename(file)

        if not file_name:
            # If secure_filename returns empty string
            file_name = ''.join(choice(ascii_letters + digits) for _ in range(10)) + Path(file).suffix

        meme_ = MemeModel(current_user.id,
                          file_name,
                          upload_form.meme_name_label.data,
                          upload_form.genre_label.data)

        try:
            meme_.save_to_cloud(upload_form.img_url.data, current_user.username, int(uuid4()))
            meme_.save_to_db()

        except Error:
            meme_.delete_from_db()

        finally:
            return redirect(url_for('user.profile', username=current_user.username))

    return render_template('meme/upload.html', form=upload_form)
