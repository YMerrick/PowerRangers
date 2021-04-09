from flask import render_template
from flask import Flask, request, url_for, redirect
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

#In order to get data from the database, need to query before hand and then pass the JSON data to it
#If we want to do searches and sort by certain aspects of the database then we have to reload the page with a condition in the query to return the data with
#This just means we have to call the page again with a post this time 
@app.route('/')
def index():
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

@app.route('/movieDetails')
def movieDetails():
    movieGenres = dbmodel.getGenres()
    genre = request.args.get('genre')
    if genre == "None":
        genre = None
    movies = dbmodel.getMovieFromGenre(genre)
    return render_template('movieList.html', 
                           title = 'Movie Details',all_movies = movies, genres = movieGenres)

@app.route('/ticket')
def ticket():
    return render_template('Printable Ticket.html',
                           title = 'The Ticket')

@app.route('/addUser', methods = ['POST','GET'])
def addMember():
    members = dbmodel.getMemberTable()
    if request.method == 'POST':
        result = request.form
        memberTable = dbmodel.MemberTable
        email = result.get('email')
        creditCard = int(result.get('creditCard'))
        password = result.get ('password')
        new_member = memberTable(walletBalance=0,email=email,creditCard=creditCard,password=password)
        dbmodel.addMemberTableEntry(new_member)
        return render_template('memberList.html',all_member = members)
    else:
        return render_template('addUser.html',all_member = members)

@app.route('/memberList')
def member():
    members = dbmodel.getMemberTable()
    return render_template('memberList.html',all_member = members)

@app.route('/movieInfo/<title>')
def movieInfo(title):
    movie = dbmodel.getMovieInfo(title)
    return render_template('MovieInfo.html',
                           title = 'Movie Infos',movie = movie)

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


@app.route('/movieInfo/<int:movie_id>',methods = ['POST','GET'])
def showScreening(movie_id):
    screeningTable = dbmodel.ScreeningTable
    movies = dbmodel.MoviesTable
    movie = dbmodel.getAMovie(movie_id)
    screenTable = dbmodel.ScreenTable
    screenID = dbmodel.getScreenID(int(movie_id))
    screen = dbmodel.getAScreen(screenID)
    if request.method == 'POST':
        result = request.form
        print(list(request.form.listvalues()))
    return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],movie=movie)