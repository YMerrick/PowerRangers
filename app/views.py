from flask import render_template
from flask import Flask, request, flash, session
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
#@app.route('/')
#def index():
#    dbmodel.makeTicketPdf(0)
#    movies = dbmodel.getMovieFromGenre()
#    return render_template('movieList.html',
#                           title='Movie List', all_movies = movies)

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


@app.route('/print')
def printTicket():
    #ticket generator
    ticketInfo = dbmodel.getBookingInfoForTicket('0')    
    return render_template('print.html',
                           title = 'Test Ticket',ticket = ticketInfo)


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
        
#shows the cinema to book a ticket
#this is a bete function just to make the website work
#used screeningID as 1 as default
#will populate screeningID and make it work with it
@app.route('/movieInfo/<int:movie_id>',methods = ['POST','GET'])
def showScreening(movie_id):
    screeningTable = dbmodel.ScreeningTable
    all_bookings = dbmodel.getBookingTable()
    movie = dbmodel.getAMovie(movie_id)
    screenTable = dbmodel.ScreenTable
    bookingTable = dbmodel.BookingTable
    screenID = dbmodel.getScreenID(int(movie_id))
    screen = dbmodel.getAScreen(screenID)
    if request.method == 'POST':
        result = request.form
        resultList = list(request.form.listvalues())
        resultList = resultList[0]
        resultList = resultList[0].split(",")
        for row in resultList:
            rowID = dbmodel.rowIDFinder(screenID,int(row))
            new_booking = bookingTable(seatNumber=row,rowID=rowID,screeningID=1,seatStatus=1,row="")
            dbmodel.addBooking(new_booking)
        return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],movie=movie,bookings=all_bookings)
    return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],movie=movie,bookings=all_bookings)

@app.route('/addFunds/<int:id>',methods = ['POST','GET'])
def addWallet(id):
    all_members = dbmodel.getMemberTable()
    user = dbmodel.getMember(id)
    if request.method == 'POST':
        result = request.form
        balance = int(result.get('wallet'))
        wallet = int(user.walletBalance)
        wallet = balance + wallet
        user.walletBalance = str(wallet)
        dbmodel.db.session.commit()
        return render_template("addFunds.html",userOut = user)
    return render_template("addFunds.html",userOut = user)

@app.route('/addFunds/<int:id>/pay',methods = ['POST','GET'])
def payTickets(id):
    user = dbmodel.getMember(id)
    if request.method == 'POST':
        result = request.form
        price = int(result.get('price'))
        balance = int(user.walletBalance)
        if(int(user.walletBalance) < price):
            message ="you don't have enough balance"
        else:
            balance = balance - price
            user.walletBalance = str(balance)
            message ="payment successful"
            return render_template("pay.html",userOut = user,messageOut = message)
        dbmodel.db.session.commit()
        return render_template("pay.html",userOut = user,messageOut = message)
    return render_template("pay.html",userOut = user)


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
        email = result.get('email')
        member = dbmodel.getUserFromEmail(email)
        if member:
            flash("User with the same email has been found.")
            #if a user with the same email is found, show error
            return render_template('signup.html')
        else:
            card = result.get('card')
            print(type(card))
            pass1 = generate_password_hash(result.get('password'), method='sha256')
            pass2 = result.get('c_password')
            if(check_password_hash(pass1, pass2)):
                new_member = memberTable(email=email,walletBalance=000.00,creditCard=card,password=pass1)
                dbmodel.addMember(new_member)
                return redirect(url_for('members'))
            else:
                flash("Password don't match")
                return render_template('signup.html')

    return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = request.form
        #memberTable = dbmodel.MemberTable
        #members = dbmodel.getMemberTable()
        member = dbmodel.getUserFromEmail(result.get('email'))
        if member:
            if(check_password_hash(member.password, result.get('password'))):
                session['logged_in'] = True
                session['id'] = member.memberID
                flash("Successful login")
                return render_template('index.html')
            else:
                flash('Invalid password provided')
                return render_template('signin.html')
        else:
            flash("User not found")
            return render_template('signin.html')
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['id'] = None
    return render_template('index.html')

@app.route('/index')
def indexTest():
    if(session['logged_in'] == True):
        flash(session['id'])
    return render_template('index.html')

@app.route('/payment')
def paymentPage():
    return render_template('Paymentpage.html')

@app.route('/addFunds')
def addFunds(member_id):
    return render_template('addFunds.html')