from src.db import db


class MemeModel(db.Model):
    __tablename__ = 'meme'

    meme_name = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    genre = db.Column(db.String(80))
    info = db.Column(db.Text(200))
    favorite = db.Column(db.String(80))
    likes = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to link items & stores
    user = db.relationship('UserModel')  # Now no joins necessary

    def __init__(self, meme_name, img_url, owner, genre=None, info=None,
                 favorite=None, likes=None, user_id=user_id, user=user):
        self.meme_name = meme_name
        self.img_url = img_url
        self.owner = owner
        self.user_id = user_id
        self.user = user

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
