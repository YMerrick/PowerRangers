from flask import render_template
from flask import Flask, request
from flask import url_for, redirect
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .models import Models
from werkzeug.security import generate_password_hash, check_password_hash

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

#In order to get data from the database, need to query before hand and then pass the JSON data to it
#If we want to do searches and sort by certain aspects of the database then we have to reload the page with a condition in the query to return the data with
#This just means we have to call the page again with a post this time
@app.route('/')
def index():
    dbmodel.makeTicketPdf(1)
    movies = dbmodel.getMovieFromGenre()
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

@app.route('/movieDetails', methods = ['POST' ,'GET'])
def movieDetails():
    if request.method == "POST":
        genre = request.form.get("selectGenre")
        movieID = request.form.get("movie")
        if genre == "":
            genre = None
        else:
            genreList = dbmodel.getMovieFromGenre(genre)
            return render_template('Movie Details.html', title = 'Movie Details', movies = genreList)
        if movieID != None:
            return redirect(url_for('movieInfo', movie=movieID))
    movies = dbmodel.getMovieFromGenre()
    return render_template('Movie Details.html',
                           title = 'Movie Details',movies = movies)

@app.route('/ticketTest')
def ticketTest():
    #returns movie title, screen name, screening time and date, seat number and, row
    ticketInfo = dbmodel.getBookingInfoForTicket('0')    
    return render_template('ticket.html',
                           title = 'Test Ticket',ticket = ticketInfo)


@app.route('/ticket')
def ticket():
    return render_template('Printable Ticket.html',
                           title = 'The Ticket')

@app.route('/movieInfo')
def movieInfo():
    movieId = request.args.get('movie')
    movies = dbmodel.getMoviesTable(movieId)
    return render_template('MovieInfo.html',
                           title = 'Movie Info', row = movies)

@app.route('/genre', methods = ['POST','GET'])
def genre():
    if request.method == 'POST':
        result = request.form
        genreTable = dbmodel.GenreTable
        genreDesc = result.get('genre')
        print(genreDesc)
        newGenre = genreTable(genreDesc = genreDesc)
        dbmodel.addGenre(newGenre)
    return render_template('genre.html',
                           genres = dbmodel.getGenres())

@app.route('/addMovie')
def addMovie():
    return render_template('addMovie.html',
                           genres = dbmodel.getGenres())

@app.route('/movieAdded', methods = ['POST','GET'])
def movieAdded():
    if request.method == 'POST':
        result = request.form
        moviesTable = dbmodel.MoviesTable
        movies = dbmodel.getMoviesTable()
        title = result.get('title')
        blurb = result.get('blurb')
        certificate = result.get('certificate')
        genre = result.getlist('genre')
        director=result.get('director')
        actorList=result.get('actorList')
        imagePath=result.get('imagePath')
        trailerLink=result.get('trailerLink')
        new_movie = moviesTable(title=title,blurb=blurb,certificate=certificate,director=director,actorList=actorList)
        dbmodel.addMoviesTableEntry(new_movie,genre)
        return render_template('movieList.html',all_movies = movies)
    else:
        return index()

@app.route('/members')
def members():
    members = dbmodel.getMemberTable()
    return render_template('memberTable.html', all_members = members)

@app.route('/signup', methods = ['GET', 'POST'])
def register():
    # needs to add validation, to make sure no existing user register again/no same credit cards are used
    if request.method == 'POST':
        result = request.form
        memberTable = dbmodel.MemberTable
        members = dbmodel.getMemberTable()
        email = result.get('email')
        card = result.get('card')
        pass1 = generate_password_hash(result.get('password'), method='sha256')
        pass2 = result.get('c_password')
        if(check_password_hash(pass1, pass2)):
            new_member = memberTable(email=email,walletBalance=000.00,creditCard=card,password=pass1)
            dbmodel.addMember(new_member)
            return redirect(url_for('members'))
        else:
            print("password dont match")

    return render_template('signup.html')

