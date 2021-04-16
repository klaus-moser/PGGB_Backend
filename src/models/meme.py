from datetime import datetime
from os import environ
from cloudinary.api import delete_resources, delete_folder
from cloudinary import uploader
from cloudinary.exceptions import Error
from typing import List

from src.db import db


class MemeModel(db.Model):
    __tablename__ = 'memes'

    id = db.Column(db.Integer, primary_key=True)
    meme_name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255))
    public_id = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.Integer)
    info = db.Column(db.Text(255))
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

    def __init__(self, owner_id, img_url, meme_name, genre=None, info=None, public_id=None):
        self.owner_id = owner_id
        self.img_url = img_url
        self.meme_name = meme_name
        self.public_id = public_id
        self.genre = genre
        self.info = info

    @classmethod
    def find_all_by_id(cls, id_: int) -> List["MemeModel"]:
        """
        Find an meme by its owner id.

        :param id_: Owner id_ to find.
        :return: Objects of Meme-class with owner id_.
        """
        return cls.query.filter_by(owner_id=id_).all()

    # TODO: def find_by_id() to find a single meme

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

    def save_to_cloud(self, image: str, username: str, pk: int) -> None:
        """
        Upload a new meme to the cloudinary cloud.

        :param image: Given image path
        :param username: String of username
        :param pk: UUID for avoiding overwriting
        """

        # Create folder for every user to store memes
        self.public_id = f'user_uploads/{username}/{pk}'

        res = uploader.upload(image, public_id=self.public_id, overwrite=True)

        endpoint = environ.get('CLOUD_ENDPOINT')
        version = f"/v{res['version']}/"
        public_id_ = res['public_id']
        image_format = res['format']

        # Update image url
        self.img_url = f"{endpoint}{version}{public_id_}.{image_format}"

    def delete_meme_from_cloud(self) -> None:
        """
        Delete meme from cloud.
        """
        uploader.destroy(public_id=self.public_id)

    @staticmethod
    def delete_folder_from_cloud(username: str) -> None:
        """
        Delete folder of user from cloud.
        Folder MUST be emptied before!
        """
        delete_folder(path=f'user_uploads/{username}')