from datetime import datetime
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

    # user = db.relationship('UserModel', backref='mememodel', foreign_keys=[owner_id, fav_by_id, like_by_id])

    #owner = db.relationship('UserModel', foreign_keys=[owner_id])
    #fav_by = db.relationship('UserModel', foreign_keys=[fav_by_id])
    #like_by = db.relationship('UserModel', foreign_keys=[like_by_id])

    def __init__(self, meme_name, owner_id):
        self.meme_name = "meme_name"
        self.owner_id = owner_id
        self.img_url = "img_url"
        self.genre = 1
        self.info = "info"
        self.likes = 0
        self.upload_date = datetime.utcnow()

    @classmethod
    def find_by_name(cls, name: str) -> object:
        """
        Find an meme by its name.

        :param name: Meme name to find.
        :return: Object of Meme-class.
        """
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls) -> dict:
        """
        Returns all memes in .db

        :return: All memes found in .db
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
