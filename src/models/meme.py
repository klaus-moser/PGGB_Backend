from datetime import datetime
from owncloud import Client, ResponseError

from src.db import db


class MemeModel(db.Model):
    __tablename__ = 'memes'

    id = db.Column(db.Integer, primary_key=True)
    meme_name = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(255))
    genre = db.Column(db.Integer)
    info = db.Column(db.Text(200))
    likes = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fav_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    like_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # TODO: check????
    # user = db.relationship('UserModel', backref='mememodel', foreign_keys=[owner_id, fav_by_id, like_by_id])
    # TODO: check????
    owner = db.relationship('UserModel', foreign_keys=[owner_id])
    fav_by = db.relationship('UserModel', foreign_keys=[fav_by_id])
    like_by = db.relationship('UserModel', foreign_keys=[like_by_id])

    def __init__(self, owner_id, img_url, meme_name, genre=None, info=None):
        self.owner_id = owner_id
        self.img_url = img_url
        self.meme_name = meme_name
        self.genre = genre
        self.info = info
        self.upload_date = datetime.utcnow()  # TODO: wrong timestamp

    @staticmethod
    def upload_image(file_path: str) -> None:
        """
        Upload image to ownCLoud shared folder

        :param file_path: String of the file in /upload/
        """
        # TODO: ssl certificate
        # Link to shared folder on ownCLoud
        pub_link = f'https://picloudserver.selfhost.co/index.php/s/TTxUVZdyxeuQ8h9'

        try:
            oc = Client.from_public_link(pub_link)
            oc.drop_file(file_name=file_path)
        except Exception as err:
            raise ResponseError("Error during upload", errorType=err) from err

    @classmethod
    def find_by_id(cls, id_: int):
        """
        Find an meme by its name.

        :param id_: Meme id_ to find.
        :return: Objects of Meme-class with id_.
        """
        return cls.query.filter_by(owner_id=id_).all()

    @classmethod
    def find_all(cls):
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
