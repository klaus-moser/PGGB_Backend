from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user
from os import remove
from werkzeug.utils import secure_filename

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
        meme_ = MemeModel(current_user.id,
                          upload_form.meme_name_label.data,
                          upload_form.img_url.data.filename,
                          upload_form.genre_label.data,
                          upload_form.info_label.data)
        meme_.save_to_db()

        filename = upload_form.img_url.data.filename
        try:
            upload_form.img_url.data.save('static/images/upload/' + filename)
        except PermissionError:
            return redirect(url_for('meme/upload'))

        upload_path = 'static/images/upload/' + filename

        try:
            meme_.upload_image(upload_path)
            remove(upload_path)
        except Exception:
            # TODO: remove entry in db
            return redirect(url_for('meme.upload'))
        return redirect(url_for('user.profile', username=current_user.username))

    return render_template('meme/upload.html', form=upload_form)
