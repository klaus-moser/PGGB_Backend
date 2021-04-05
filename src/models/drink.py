from src.db import db

# TODO:
class DrinkModel(db.Model):
    __tablename__ = 'drinks'

    name = db.Column(db.String(80), nullable=False)
    inventor = db.Column(db.String(80))
    type = db.Column(db.String(80))
    about = db.Column(db.Text(200))
    favorite = db.Column(db.String(80))
    likes = db.Column(db.Integer)

    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.password = hashed_password