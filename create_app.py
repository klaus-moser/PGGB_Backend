from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager

from src.models.user import UserModel
from src.resources.main import main
from src.resources.user import user
from src.resources.meme import meme

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
    app.config.from_object("src.config." + modes[mode])
    app.app_context().push()

    # Initialization of .db & loginManager
    db.init_app(app=app)
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

    @login_manager.unauthorized_handler
    def unauthorized():
        """
        Redirect to '/login' if user is not logged in.
        """
        # TODO: flash("Please sign in to access", 'red')
        return redirect(url_for("user.login"))

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
    app.register_blueprint(meme)

    return app
