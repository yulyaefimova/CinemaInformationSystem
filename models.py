from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def get_id(self):
        return self.user_id
