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


class Genres(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(1000), nullable=False)


class Countries(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(1000), nullable=False)


class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("Genres.genre_id"), nullable=False)
    duration = db.Column(db.String(1000), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("Countries.country_id"), nullable=False)
    age_limit = db.Column(db.Integer, nullable=False)


class Halls(db.Model):
    hall_id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(1000), nullable=False)
    number_of_seats = db.Column(db.Integer, nullable=False)
    number_of_rows = db.Column(db.Integer, nullable=False)
    number_of_seats_in_row = db.Column(db.Integer, nullable=False)


class Sessions(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(100), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey("Halls.hall_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("Movies.movie_id"), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Tickets(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey(Sessions.session_id), nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
