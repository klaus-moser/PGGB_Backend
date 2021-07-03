from os import environ
from cloudinary import config


modes: dict = {'PRODUCTION': 'ProductionConfig',
               'DEVELOP': 'DevelopmentConfig',
               'TEST': 'TestingConfig'}


class Config(object):
    """
    Default configuration.
    'python-dotenv' is used to read the key-value pairs from a .env file
    and set them as environment variables.
    The file '.env.example' shows all variables that are needed.
    """
    ADMIN: int = 1

    ENV = 'production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')

    DB_NAME = "production-db"
    DB_USERNAME = environ.get('DB_USERNAME')
    DB_PASSWORD = environ.get('DB_PASSWORD')

    FLASK_SERVER_NAME = 'localhost:5000'
    FLASK_THREADED = True
    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # Cloudinary API Settings
    config(
        cloud_name=environ.get("CLOUD_NAME"),
        api_key=environ.get("CLOUD_API_KEY"),
        api_secret=environ.get("CLOUD_API_SECRET"),
    )
    CLOUDINARY_ROOT_FOLDER = "user_uploads"

    # Email configuration # TODO: into environ
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    # ADMINS = ['hotdogzapp@gmail.com', 'cjcon90@pm.me']


class ProductionConfig(Config):
    """
    Production configuration.
    """
    pass


class DevelopmentConfig(Config):
    """
    Development configuration.
    """
    ENV = 'development'
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "userjw"
    DB_PASSWORD = "1q2w3e4r"

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')

    SESSION_COOKIE_SECURE = False

    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """
    Testing configuration.
    """
    ENV = 'testing'
    TESTING = True

    DB_NAME = "testing-db"
    DB_USERNAME = "userjw"
    DB_PASSWORD = "1q2w3e4r"

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')

    SESSION_COOKIE_SECURE = False

    LOG_LEVEL = 'DEBUG'
