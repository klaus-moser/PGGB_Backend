from cloudinary.exceptions import Error
from string import ascii_letters, digits
from random import choice
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from uuid import uuid4
from pathlib import Path

from src.wtform_fields import UploadMemeForm
from src.models.meme import MemeModel

meme = Blueprint('meme', __name__)


@meme.route('/meme_page')
def meme_page():
    ...
    # TODO: description missing
    # TODO: dont redirect -> search fo rbetter solution
    if not current_user.is_authenticated:
        return redirect(url_for('main.gallery'))

    # TODO: add infos (likes/favs) to pictures

    # Selected meme
    selected_meme_id = int(request.args.get('selected_meme'))

    # Selected meme in front
    memes = [MemeModel.find_by_id(selected_meme_id)]

    # Append all other memes
    for meme_ in current_user.memes:
        if meme_.id != selected_meme_id:
            memes.append(meme_)

    return render_template('meme/meme.html', memes=memes)


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
def edit(meme_id):
    # TODO: edit meme
    return f'{meme_id}'


@meme.route('/delete_meme/<meme_id>', methods=["POST", "GET"])
@login_required
def delete(meme_id):
    # TODO: delete meme
    return f'{meme_id}'
