from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from src.models.user import UserModel
from src.resources.main import main
from src.resources.user import user


from src.blacklist import BLACKLIST
from src.config import modes
from src.db import db


def create_app(mode: str = 'DEPLOY') -> Flask:
    """
    Creates a Flask app with a specific configuration (Default: PRODUCTION.)

    :param mode: 'PRODUCTION', 'DEVELOP', 'TEST'
    :return: Flask app.
    """
    app = Flask(__name__)

    # Check mode
    if mode not in modes:
        mode = 'DEPLOY'

    # Load config
    app.config.from_object("config." + modes[mode])
    app.app_context().push()

    # Initialization of .db, JWT & loginManager
    db.init_app(app=app)
    jwt = JWTManager(app=app)

    login_manager = LoginManager()
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(user_id: str) -> object:
        """
        Load a user when he logs in an give it to the login_manager.
        :param user_id: Userid.
        :return: User object.
        """
        return UserModel.find_by_id(id_=user_id)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity: int) -> dict:
        """
        Whenever we create a new JWT-token, this function is called to check,
        if we should add any extra data ("claims") to that JWT as well.

        :param identity: Int of the user-id.
        :return: {'is_admin': Bool}
        """
        if identity == app.config['ADMIN']:
            return {'is_admin': True}
        return {'is_admin': False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_headers, jwt_payload):
        """
        Check it 'jti' is in the BLACKLIST set().
        If true, request will be reverted to the 'revoked_token_callback'.
        """
        return jwt_payload['jti'] in BLACKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_headers, jwt_payload):
        return jsonify({
            'description': 'The token has expired.',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed.',
            'error': 'token_invalid'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain any access token.',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_headers, jwt_payload):
        return jsonify({
            'description': 'Token is NOT fresh.',
            'error': 'fresh_token_required'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_headers, jwt_payload):
        return jsonify({
            'description': 'Token has been revoked.',
            'error': 'token_revoked'
        }), 401

    @app.before_first_request
    def create_tables() -> None:
        """
        Creates all the tables (it sees) in a .db file.
        """
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(error) -> tuple:
        return render_template('error/error-404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error) -> tuple:
        return render_template('error/error-500.html'), 500

    # Endpoints
    app.register_blueprint(main)
    app.register_blueprint(user)

    return app
