from os import environ
from os.path import dirname, join
from datetime import timedelta


modes: dict = {'PRODUCTION': 'ProductionConfig',
               'DEVELOP': 'DevelopmentConfig',
               'TEST': 'TestingConfig'}


class Config(object):
    """
    Default configuration.
    """
    ADMIN: int = 1

    ENV = 'production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"  # TODO: *** Change ***

    DB_NAME = "production-db"
    DB_USERNAME = "foo"  # TODO: *** Change ***
    DB_PASSWORD = "bar"  # TODO: *** Change ***

    SESSION_COOKIE_SECURE = True

    FLASK_SERVER_NAME = 'localhost:5000'
    FLASK_THREADED = True

    JWT_SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"  # TODO: *** Change ***
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=120)
    JWT_COOKIE_SECURE = False
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///' + DB_NAME + '.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True


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
