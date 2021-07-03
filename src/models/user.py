from datetime import datetime
from flask_login import UserMixin
import cloudinary.exceptions
from cloudinary import uploader

from src.db import db
from config import Config


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80))
    img_url = db.Column(db.String(255))
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    memes = db.relationship(
        "MemeModel", back_populates="owner",
        cascade="all, delete",
        passive_deletes=True
    )

    def __init__(self, username, email, hashed_password, img_url=None):
        self.username = username
        self.email = email
        self.password = hashed_password
        self.img_url = img_url
        self.register_date = datetime.utcnow()

    def json(self) -> dict:
        """
        Returns the id & name as .json string.

        :return: {'id': Int, 'username': String}
        """
        return {'id': self.id, 'username': self.username, 'email': self.email}

    @classmethod
    def find_by_username(cls, username: str) -> object:
        """
        Find an (already registered) user by the given username.

        :param username: Username to search for the user.
        :return: Object of the User class.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> object:
        """
        Find an (already registered) user by the given email.

        :param email: Email to search for the user.
        :return: Object of the User class.
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id_: str) -> object:
        """
        Find a (already registered) use by the given id.

        :param id_: ID to search for the user.
        :return: Object of the User class.
        """
        return cls.query.get(id_)

    def save_to_db(self) -> None:
        """
        Save user to data base.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete user from database.
        """
        db.session.delete(self)
        db.session.commit()
