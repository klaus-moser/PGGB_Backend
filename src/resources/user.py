import cloudinary.exceptions
from flask import render_template, make_response, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, current_user, login_required
from passlib.hash import pbkdf2_sha256
from random import randint
from os import environ
from uuid import uuid4
from copy import deepcopy

from src.models.user import UserModel
from src.models.meme import MemeModel
from src.wtform_fields import (RegisterForm,
                               LoginForm,
                               DeleteAccountForm,
                               EditProfileForm)

user = Blueprint('user', __name__)


@user.route('/register', methods=["GET", "POST"])
def register():
    """
    Register a new user.
    """

    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        # Hashing: incl. 16-byte salt (auto) + 29.000 iterations (default)
        hashed_password = pbkdf2_sha256.hash(password)

        # Set a random avatar
        avatar_url = (environ.get('URL_AVATARS') + f'{randint(1, 20)}.png')

        user_ = UserModel(username, email, hashed_password, avatar_url)
        user_.save_to_db()

        login_user(user_)
        return redirect(url_for('user.select_avatar'))

    return make_response(render_template('user/register.html', form=register_form), 200)


@user.route('/login', methods=["GET", "POST"])
def login():
    """
    Login a new user.
    """

    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():

        user_ = UserModel.find_by_username(login_form.username.data)

        if user_ and pbkdf2_sha256.verify(login_form.password.data, user_.password):
            # Login
            login_user(user=user_)
            return redirect(url_for('main.gallery'))
        # User unknown or wrong password
        return redirect(url_for('user.login'))
    # GET
    return make_response(render_template('user/login.html', form=login_form), 200)


@user.route('/profile/<username>', methods=["GET"])
@login_required
def profile(username: str):
    """
    Show user profile.

    :param username: String with current user.
    """

    user_ = UserModel.find_by_username(username)

    # Memes
    meme_models = MemeModel.find_all_by_id(id_=user_.id)
    memes = [meme for meme in meme_models]
    if not memes:
        memes = None

    # TODO: bug: "GET /profile/None HTTP/1.1" 200
    # https://github.com/klaus-moser/PGGB_Backend/issues/14

    return make_response(render_template('user/profile.html',
                                         title=f"{user_.username}",
                                         user=user_,
                                         memes=memes,
                                         favorites=None))


@user.route('/logout')
@login_required
def logout():
    """
    Logout user.
    """

    logout_user()
    return redirect(url_for('main.index'))


@user.route('/reset_password', methods=["GET", "POST"])
@login_required
# TODO: implement reset_password()
def reset_password():
    """
    Reset user password.
    """
    return make_response(render_template('error/error-404.html'))


@user.route('/delete_account/<user_id>', methods=["GET", "POST"])
@login_required
def delete_account(user_id):
    """
    Delete a user from the db.
    This also deletes all user memes on the cloud!
    """

    user_ = UserModel.find_by_id(id_=user_id)

    if user_ != current_user and current_user != 'admin':
        redirect(url_for('main.gallery'))

    delete_form = DeleteAccountForm()
    if delete_form.validate_on_submit():

        if not pbkdf2_sha256.verify(delete_form.password.data, user_.password):
            return redirect(url_for('user.profile', username=user_.username))

        else:
            if current_user != 'admin':
                # Save logout user
                logout_user()

                # Delete all memes from cloud
                memes = MemeModel.find_all_by_id(user_id)
                for meme in memes:
                    meme.delete_meme_from_cloud()

                # Delete empty user-folder from cloud
                MemeModel.delete_folder_from_cloud(username=user_.username)

                # Delete all user data from .db
                user_.delete_from_db()

                return redirect(url_for('main.index'))

    return make_response(render_template('user/delete_account.html',
                                         title="Delete account",
                                         user=user_,
                                         form=delete_form), 200)


@user.route('/edit_profile/<user_id>', methods=["GET", "POST"])
@login_required
def edit_profile(user_id):
    """
    Edit a user.
    """
    
    user_ = UserModel.find_by_id(user_id)
    if user_ != current_user and current_user.username != 'admin':
        return redirect(url_for('main.gallery'))

    edit_form = EditProfileForm()

    if edit_form.is_submitted():

        # Check if username is different
        if edit_form.username.data != user_.username and not edit_form.validate_username(username=edit_form.username):

            # Migrate files on cloudinary to new folder with new public_id
            memes_ = MemeModel.find_all_by_id(id_=user_id)
            memes_save = deepcopy(memes_)

            try:
                for meme_ in memes_:
                    # Save to new folder in cloud
                    meme_.save_to_cloud(meme_.img_url, edit_form.username.data, int(uuid4()))
                    # Update .db
                    meme_.save_to_db()

            except cloudinary.exceptions.Error as err:
                print(err)

            try:
                # Delete all memes from old folder
                for meme in memes_save:
                    meme.delete_meme_from_cloud()

                # Delete empty folder
                MemeModel.delete_folder_from_cloud(username=user_.username)

                # change
                user_.username = edit_form.username.data
                user_.save_to_db()

            except cloudinary.exceptions.Error as err:
                print(err)

        # Check if email is different
        if edit_form.email.data != user_.email and not edit_form.validate_email(email=edit_form.email):
            # Change
            user_.email = edit_form.email.data
            user_.save_to_db()

        return redirect(url_for('user.profile', username=user_.username))

    else:
        # Fill out boxes with user data
        edit_form.username.data = user_.username
        edit_form.email.data = user_.email

    return render_template('user/edit_profile.html', title='Edit Profile',
                           user=user_, form=edit_form)


@user.route('/select_avatar/', methods=["GET"])
@login_required
def select_avatar():
    """
    Edit the user's avatar.
    """

    if request.args.get('selected_avatar'):
        user_ = UserModel.find_by_username(current_user.username)

        user_.img_url = request.args.get('selected_avatar')
        user_.save_to_db()
        return redirect(url_for('user.profile', username=user_.username))

    # Avatar urls
    avatars = [environ.get('URL_AVATARS') + f'{i}.png' for i in range(1, 21)]

    return render_template('user/select_avatar.html', avatars=avatars,
                           title='Choose Avatar')
