from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    This code is needed for SQLite to activate the foreign key support:

    https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Database object
db = SQLAlchemy()
