from datetime import datetime
from os import environ
from cloudinary import uploader
from typing import List

from src.db import db


class MemeModel(db.Model):
    __tablename__ = 'memes'

    id = db.Column(db.Integer, primary_key=True)
    meme_name = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(255))
    genre = db.Column(db.Integer)
    info = db.Column(db.Text(200))
    likes = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # TODO:
    # users = db.relationship('UserModel', lazy=True, foreign_keys=[id])
    # users = db.relationship('UserModel')

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    # fav_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    # like_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

    owner = db.relationship('UserModel', back_populates="memes")
    # fav_by = db.relationship('UserModel', back_populates="children")
    # like_by = db.relationship('UserModel', back_populates="children")

    def __init__(self, owner_id, img_url, meme_name, genre=None, info=None):
        self.owner_id = owner_id
        self.img_url = img_url
        self.meme_name = meme_name
        self.genre = genre
        self.info = info

    @staticmethod
    def upload_image(image: str, username: str, pk: int) -> None:
        # TODO: DOC
        # Create folder for every user to store memes
        folder_id = f'user_uploads/{username}/{pk}'

        try:
            res = uploader.upload(image, public_id=folder_id, overwrite=True)
            cloud_name = environ.get('CLOUD_NAME')
            endpoint = environ.get('CLOUD_ENDPOINT')

        except Exception as err:
            pass  # TODO

    @classmethod
    def find_by_id(cls, id_: int) -> List["MemeModel"]:
        """
        Find an meme by its name.

        :param id_: Meme id_ to find.
        :return: Objects of Meme-class with id_.
        """
        return cls.query.filter_by(owner_id=id_).all()

    @classmethod
    def find_all(cls) -> List["MemeModel"]:
        """
        Returns all memes in .db
        """
        return cls.query.all()

    def save_to_db(self) -> None:
        """
        Save meme to data base.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete meme from database.
        """
        db.session.delete(self)
        db.session.commit()
