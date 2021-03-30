from flask import render_template
from flask import Flask
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .models import Models

dbmodel = Models()

#Moved this to models.py and created it as a class instead to get a working api
'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
MoviesTable = Base.classes.MoviesTable
BookingTable = Base.classes.BookingTable
CustomerTable = Base.classes.CustomerTable
MemberTable = Base.classes.MemberTable
PaymentTable = Base.classes.PaymentTable
ScreeningTable = Base.classes.ScreeningTable
ScreenTable = Base.classes.ScreenTable
SeatTable = Base.classes.SeatTable
TicketTable = Base.classes.TicketTable'''


@app.route('/')
def index():
    movies = dbmodel.getMoviesTable()
    return render_template('movieList.html',
                           title='Movie List', all_movies = movies)

@app.route('/cinemaSeats')
def cinemaSeat():
    return render_template('CinemaSeat.html', 
                           title = 'Pick your seats')

@app.route('/MainPage')
def mainPage():
    return render_template('MainPage.html',
                           title = 'The Main Page')

@app.route('/movieDetails')
def movieDetails():
    return render_template('Movie Details.html', 
                           title = 'Movie Details')

@app.route('/ticket')
def ticket():
    return render_template('Printable Ticket.html',
                           title = 'The Ticket')

@app.route('/movieInfo')
def movieInfo():
    return render_template('MovieInfo.html',
                           title = 'Movie Infos')