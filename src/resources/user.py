from flask import render_template, make_response, redirect
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                get_jwt)

from src.models.user import UserModel
from src.blacklist import BLACKLIST
from src.wtform_fields import RegisterForm, LoginForm


class UserRegister(Resource):
    """
    Class to register a new user.
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

    @staticmethod
    def get():
        """
        Render the 'register.html'.

        :return: 'register'
        """
        register_form = RegisterForm()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html', form=register_form), 200, headers)

    @classmethod
    def post(cls) -> tuple:
        """
        Add a new user to the data base.

        :return: {json_message}, status code
        """
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user '{}' already exists!".format(data['username'])}, 400

        elif data['password'] != data['confirm_pwd']:
            return {"message": "Passwords do not match!"}, 401

        data['password'] = pbkdf2_sha256.hash(data['password'])

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    # TODO: @jwt_required()
    def get(cls, user_id) -> tuple:
        """
        Get the user by an id.

        :param user_id: Integer of userid.
        :return: User or .json message
        """
        user = UserModel.find_by_id(id_=user_id)

        if not user:
            return {'message': 'User not found!'}, 404
        return user.json(), 200

    @classmethod
    # TODO: @jwt_required(fresh=True)
    def delete(cls, user_id) -> tuple:
        """
        Delete a user from the db.
        Requires a fresh JWT.

        :param user_id: Int of user id.
        :return: .json message + status code.
        """
        user = UserModel.find_by_id(id_=user_id)

        if not user:
            return {'message': 'User not found!'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
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

    @staticmethod
    def get():
        """
        Render the login.html page.

        :return: login.html
        """
        login_form = LoginForm()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html', form=login_form), 200, headers)

    @classmethod
    def post(cls) -> tuple:
        """
        Login a user with username and password.
        Additionally create the 'access_token' & 'refresh_token'.

        :return: Token (access & refresh) or info message.
        """
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and pbkdf2_sha256.verify(data['password'], user.password):
            # create access token + save user.id in that token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(identity=user.id)

            headers = {'Authorization': 'Bearer ' + access_token}
            response = make_response(render_template('gallery.html'), 200, headers)

            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)

            return response

        return {'message': 'Invalid credentials!'}, 401



class UserLogout(Resource):

    @jwt_required()
    def post(self) -> tuple:
        """
        Put jti on the BLACKLIST to deny further access to endpoints.

        :return: {'message': 'Successfully logged out!'}, 200
        """
        jti = get_jwt()['jti']  # jti = "JWT ID", a unique identifier for a JWT.

        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out!'}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self) -> tuple:
        """
        Refresh an existing (access-)token.

        :return: {'access_token': new_token} BUT:(fresh=False), 200
        """
        current_user = get_jwt_identity()

        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
