from flask import Blueprint, redirect, url_for, render_template, request, make_response
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from string import ascii_letters, digits
from cloudinary.exceptions import Error
from random import choice
from pathlib import Path
from uuid import uuid4

from src.wtform_fields import UploadMemeForm, DeleteMemeForm
from src.models.meme import MemeModel

meme = Blueprint('meme', __name__)


@meme.route('/meme_page')
def meme_page():
    """
    This is the main page of the selected meme.

    :return: renders the 'meme/meme.html' template including the selected meme.
    """

    # Selected meme
    selected_meme_id = int(request.args.get('selected_meme'))

    # Selected meme in front
    meme_ = MemeModel.find_by_id(selected_meme_id)

    return render_template('meme/meme.html', meme=meme_)


@meme.route('/upload', methods=["POST", "GET"])
@login_required
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


@meme.route('/edit_meme/<meme_id>', methods=["POST", "GET"])
@login_required
def edit_meme(meme_id):
    # TODO: edit meme
    return f'{meme_id}'


@meme.route('/delete_meme/<meme_id>', methods=["POST", "GET"])
@login_required
def delete_meme(meme_id: int):
    """
    Delete a meme from .db and from cloud.

    :param meme_id: Integer of 'meme_id'
    """

    delete_form = DeleteMemeForm()
    meme_ = MemeModel.find_by_id(id_=meme_id)

    if request.method == 'POST':

        if delete_form.delete_button.data:
            meme_.delete_meme_from_cloud()
            meme_.delete_from_db()
        return redirect(url_for('user.profile', username=current_user.username))

    return make_response(render_template('meme/delete_meme.html', meme_id=meme_id, form=delete_form, meme=meme_))
