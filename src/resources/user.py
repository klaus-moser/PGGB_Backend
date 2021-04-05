from flask import render_template, make_response, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, logout_user
from flask_restful import reqparse
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt,
                                set_refresh_cookies,
                                set_access_cookies)

from src.models.user import UserModel
from src.blacklist import BLACKLIST
from src.wtform_fields import RegisterForm, LoginForm


user = Blueprint('user', __name__)


@user.route('/register', methods=["GET", "POST"])
def register():
    """
    Register a new user.
    """
    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'confirm_pwd',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    register_form = RegisterForm()

    if request.method == 'GET':

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user/register.html', form=register_form), 200, headers)

    else:
        data = parser.parse_args()

        # TODO: login manager?
        if UserModel.find_by_username(data['username']):
            return {"message": "A user '{}' already exists!".format(data['username'])}, 400

        # TODO: login manager?
        elif data['password'] != data['confirm_pwd']:
            return {"message": "Passwords do not match!"}, 401

        data['password'] = pbkdf2_sha256.hash(data['password'])

        user_ = UserModel(**data)
        user_.save_to_db()

        return redirect(url_for('/gallery'))


@user.route('/login', methods=["GET", "POST"])
def login():
    """
    Login a new user.
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    login_form = LoginForm()

    if request.method == 'GET':
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user/login.html', form=login_form), 200, headers)

    else:
        data = parser.parse_args()

        user_ = UserModel.find_by_username(data['username'])

        if user and pbkdf2_sha256.verify(data['password'], user_.password):
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

        return redirect(url_for('/login'))


@user.route('/logout', methods=["POST"])
def logout():
    """
    Logout user.
    """
    jti = get_jwt()['jti']
    BLACKLIST.add(jti)

    logout_user()
    flash("Logged out!", "success")
    return redirect(url_for('index'))


@user.route('/reset_password', methods=["GET", "POST"])
def reset_password():  # TODO
    """
    Reset user password.
    """
    return make_response(render_template('error/error-404.html'))


@user.route('/delete_account', methods=["GET", "POST"])
def delete_account(user_id):
    """
    Delete a user from the db.
    """
    user_ = UserModel.find_by_id(id_=user_id)

    if not user:
        # TODO: flash
        return {'message': 'User not found!'}, 404
    user_.delete_from_db()
    return redirect(url_for('/'))


"""
class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self) -> tuple:
        current_user = get_jwt_identity()

        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200  # TODO: implement make_response
"""