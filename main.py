from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import User, Movies, Genres, Countries, Halls, Sessions, Tickets
from app import db
from dateutil.relativedelta import relativedelta

main = Blueprint('main', __name__)
session_id = 0

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/poster')
@login_required
def poster():
    # rel = db.session.query(Movies, Genres).join(Movies, Genres.genre_id == Movies.genre_id)
    return render_template('poster.html', name=current_user.name, movies=db.session.query
    (Movies, Genres, Countries) \
                           .filter(Movies.genre_id == Genres.genre_id) \
                           .filter(Movies.country_id == Countries.country_id).all())


@main.route('/sessions')
@login_required
def sessions():
    return render_template('sessions.html', name=current_user.name, sessions=db.session.query
    (Sessions, Movies, Halls) \
                           .filter(Movies.movie_id == Sessions.movie_id) \
                           .filter(Halls.hall_id == Sessions.hall_id).all())


@main.route('/booking')
@login_required
def booking():
    global session_id
    session_id = int(request.args.get('session_id'))
    session = db.session.query(Sessions, Movies, Halls) \
        .filter(Movies.movie_id == Sessions.movie_id) \
        .filter(Halls.hall_id == Sessions.hall_id) \
        .filter(Sessions.session_id == int(session_id)).first()
    if relativedelta(date.today(), current_user.date_of_birth).years < \
            db.session.query(Movies).filter(Movies.movie_id == session.Movies.movie_id).first().age_limit:
        flash('Из-за возрастного ограничения Вы не можете забронировать билет')
        return redirect(url_for('main.sessions'))
    return render_template('booking.html', session=session, name=current_user.name)


@main.route('/booking', methods=['POST'])
@login_required
def booking_seat():
    global session_id
    row = int(request.form.get('select_row'))
    seat = int(request.form.get('select_seat'))

    selected_seat = Tickets.query.filter_by(seat=seat, row=row).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if selected_seat:
        flash('Это место уже занято, выберите другое')
        return redirect(url_for('main.booking_seat'))  # if user doesn't exist or password is wrong, reload the page

    ticket_id = Tickets.query.count() + 1
    # if the above check passes, then we know the user has the right credentials
    new_seat = Tickets(ticket_id=ticket_id, session_id=session_id, row=row, seat=seat,
                       user_id=current_user.user_id)

    # add the new user to the database
    db.session.add(new_seat)
    db.session.commit()
    return render_template('approve.html', name=current_user.name)

