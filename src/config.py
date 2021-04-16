from os import environ
import cloudinary
from datetime import timedelta


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

    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
    JWT_COOKIE_SECURE = False
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # Cloudinary API Settings
    cloudinary.config(
        cloud_name=environ.get("CLOUD_NAME"),
        api_key=environ.get("CLOUD_API_KEY"),
        api_secret=environ.get("CLOUD_API_SECRET")
    )


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
