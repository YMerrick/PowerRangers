from flask import render_template, Flask, request, flash, session, url_for, redirect
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .models import Models
from werkzeug.security import generate_password_hash, check_password_hash
import logging # for testing
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
    if "logged_in" in session and session["logged_in"] == True: # to check if user is online then hide the menu login and signup
        flag = "1"
        name = dbmodel.getUserFromID(session["id"])
    else:
        flag = "0"
        name = None
    genreList = dbmodel.getGenres()
    if request.method == "POST":
        genre = request.form.get("selectGenre")
        date = request.form.get("date")
        movieID = request.form.get("movie")
        if genre == "":
            if "genre" in session:
                session.pop("genre", None)
            genre = None
        else:
            session["genre"] = genre

        if date == "":
            session.pop("date", None)
        elif date != None:
            session["date"] = date
        if movieID != None:
            return redirect(url_for('movieInfo', movie=movieID))

        if "genre" in session:
            genre = session["genre"]
            if "date" in session and session["date"] != "" and session["date"] != None:
                date = session["date"]
                movieList = dbmodel.getMovie(genre=genre,date=date)
            else:
                movieList = dbmodel.getMovie(genre=genre)
            return render_template('Movie Details.html', title = 'Movie Details', movies = movieList, genreList = genreList, flag = flag, name = name)

        if "date" in session and session["date"] != "" and session["date"] != None:
            date = session["date"]
            if "genre" in session:
                genre = session["genre"]
                listFromDate = dbmodel.getMovie(genre=genre,date=date)
            else:
                listFromDate = dbmodel.getMovie(date)
            return render_template('Movie Details.html', title = 'Movie Details', movies = listFromDate, genreList = genreList, flag = flag, name = name)

    movies = dbmodel.getMovieFromGenre()
    return render_template('Movie Details.html',
                           title = 'Movie Details',movies = movies, genreList = genreList, flag = flag, name = name)

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
    if "logged_in" in session and session["logged_in"] == True:
        name = dbmodel.getUserFromID(session["id"])
    else:
        name = None
        # flash("User not found or not admin")
        # return render_template('signin.html') to check if user is not admin or online
    members = dbmodel.getMemberTable()
    if request.method == 'POST':
        result = request.form
        memberTable = dbmodel.MemberTable
        email = result.get('email')
        creditCard = int(result.get('creditCard'))
        password = result.get ('password')
        new_member = memberTable(walletBalance=0,email=email,creditCard=creditCard,password=password)
        dbmodel.addMemberTableEntry(new_member)
        return render_template('memberList.html',all_member = members, name = name)
    else:
        return render_template('addUser.html',all_member = members, name = name)

@app.route('/memberList')
def member():
    if "logged_in" in session and session["logged_in"] == True:
        name = dbmodel.getUserFromID(session["id"])
    else:
        name = None
        # flash("User not found")
        # return render_template('signin.html')
    members = dbmodel.getMemberTable()
    return render_template('memberList.html',all_member = members, name = name)

@app.route('/movieInfo')
def movieInfo():
    if "logged_in" in session and session["logged_in"] == True:
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        name = None
        flag = "0"
    movieId = request.args.get('movie')
    movies = dbmodel.getMoviesTable(movieId)
    return render_template('MovieInfo.html',
                           title = 'Movie Info', movie = movies, flag = flag, name = name)

@app.route('/genre', methods = ['POST','GET'])
def genre():
    if "logged_in" in session and session["logged_in"] == True:
        name = dbmodel.getUserFromID(session["id"])
    else:
        name = None
        # flash("User not found")
        # return render_template('signin.html')
    if request.method == 'POST':
        result = request.form
        genreTable = dbmodel.GenreTable
        genreDesc = result.get('genre')
        print(genreDesc)
        newGenre = genreTable(genreDesc = genreDesc)
        dbmodel.addGenre(newGenre)
    return render_template('genre.html',
                           genres = dbmodel.getGenres(), name = name)

@app.route('/addMovie')
def addMovie():
    if "logged_in" in session and session["logged_in"] == True:
        name = dbmodel.getUserFromID(session["id"])
    else:
        # flash("User not found")
        # return render_template('signin.html')
        name = None
    return render_template('addMovie.html',
                           genres = dbmodel.getGenres(), name = name)

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
        return url_for(redirect('/'))
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
    session.pop('_flashes', None)
    if request.method == 'POST':
        result = request.form
        memberTable = dbmodel.MemberTable
        username= request.form.get('username')
        email = request.form.get('email')
        ID = str(username)+"@"+str(email)
        member = dbmodel.getUserFromEmail(ID)
        if member:
            #if a user with the same email is found, show error
            flash("User with the same email has been found.")
            return render_template('signup.html')
        else:
            card = result.get('card')
            print(type(card))
            pass1 = generate_password_hash(result.get('password'), method='sha256')
            pass2 = result.get('c_password')
            if(check_password_hash(pass1, pass2)):
                new_member = memberTable(email=ID,walletBalance=000.00,creditCard=card,password=pass1)
                dbmodel.addMember(new_member)
                flash("Successfully registered")
                return render_template('signin.html')
            else:
                flash("Password don't match")
                return render_template('signup.html')
    return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    if request.method == 'POST':
        #result = request.form
        #memberTable = dbmodel.MemberTable
        #members = dbmodel.getMemberTable()
        username= request.form.get('username')
        email = request.form.get('email')
        ID = str(username)+"@"+str(email)
        member = dbmodel.getUserFromEmail(ID)
        if member:
            if(check_password_hash(member.password, request.form.get('password'))): # change result.get('password') to this as it causes error
                session['logged_in'] = True
                session['id'] = member.memberID
                session['username'] = username
                current_user = dbmodel.getUserFromID(session['id'])
                flash("Successful login")
                #return render_template('index.html', current_user = current_user)
                return redirect(url_for('movieDetails'))
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
    return redirect(url_for('movieDetails'))

@app.route('/index')
def indexTest():
    if(session['logged_in'] == True):
        current_user = dbmodel.getUserFromID(session['id'])
        return render_template('index.html', current_user = current_user)
    else:
        return render_template('index.html', current_user = None)

@app.route('/profile')
def profile():
    current_user = dbmodel.getUserFromID(session['id'])
    if(session['username'] == "admin"):
        flag = "1"
        print("is admin")
        return render_template('settings.html', flag = flag, name = current_user)
    else:
        flag = "0"
        print("is normal member")
        return render_template('settings.html', flag = flag, name = current_user)
        

@app.route('/payment')
def paymentPage():
    return render_template('Paymentpage.html')

@app.route('/addFunds')
def addFunds(member_id):
    return render_template('addFunds.html')

