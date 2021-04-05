from flask import render_template, make_response, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, logout_user
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt,
                                set_refresh_cookies,
                                set_access_cookies,
                                jwt_required)

from src.models.user import UserModel
from src.blacklist import BLACKLIST
from src.wtform_fields import RegisterForm, LoginForm


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

        user_ = UserModel(username, email, hashed_password)
        user_.save_to_db()

        login_user(user_)
        return redirect(url_for('main.gallery'))

    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('user/register.html', form=register_form), 200, headers)


@user.route('/login', methods=["GET", "POST"])
def login():
    """
    Login a new user.
    """
    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():

        user_ = UserModel.find_by_username(login_form.username.data)

        if user and pbkdf2_sha256.verify(login_form.password.data, user_.password):
            # Login
            login_user(user=user_)
            flash(f"Welcome back, {user_.username}!", "success")

            # create access & refresh token + save user.id in that token
            access_token = create_access_token(identity=user_.id, fresh=True)
            refresh_token = create_refresh_token(identity=user_.id)

            response = make_response(render_template('main/gallery.html'), 200)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        # User unknown or wrong password
        flash('Invalid username or password', 'error')
        return redirect(url_for('user.login'))
    # Get
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('user/login.html', form=login_form), 200, headers)


@user.route('/profile/<username>', methods=["GET"])
def profile(username):  # TODO: return user profile
    """
    Show user profile.

    :param username: String with current user.
    """
    user = UserModel.find_by_username(username)
    return render_template('user/profile.html', title=f"{user.username}", user=user)


@user.route('/logout')
@jwt_required()
def logout():
    """
    Logout user.
    """
    jti = get_jwt()['jti']
    BLACKLIST.add(jti)

    logout_user()
    flash("Logged out!", "success")
    return redirect(url_for('main.index'))


@user.route('/reset_password', methods=["GET", "POST"])
def reset_password():  # TODO
    """
    Reset user password.
    """
    return make_response(render_template('error/error-404.html'))


@user.route('/delete_account/<user_id>', methods=["GET", "POST"])
def delete_account(user_id):  # TODO:
    """
    Delete a user from the db.
    """
    user_ = UserModel.find_by_id(id_=user_id)

    if not user:
        return {'message': 'User not found!'}, 404
    user_.delete_from_db()
    return redirect(url_for('/'))


@user.route('/edit_profile/<user_id>', methods=["GET", "POST"])
def edit_profile(user_id):  # TODO:
    """
    Delete a user from the db.
    """
    return "hello world"
