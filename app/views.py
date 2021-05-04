from flask import render_template, Flask, request, flash, session, url_for, redirect
from flask_qrcode import QRcode
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .models import Models
from werkzeug.security import generate_password_hash, check_password_hash
import logging # for testing
dbmodel = Models()
QRcode(app)
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
    #dbmodel.makeTicketPdf(0)
    movies = dbmodel.getMovie()
    rows = dbmodel.getRowForScreening(1)
    booked = dbmodel.getBookingInfoForScreening(3)
    for seats in booked:
        print(seats.rowNumber,seats.seatCount)
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
    session.pop('_flashes', None)
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
        time = request.form.get('time')
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
            session["movie"] = movieID
            return redirect(url_for('movieInfo', movie=movieID))
        if time != None:
            if time != "" :
                session["movie"] = time
                return redirect(url_for('timeSelection'))
        if "genre" in session:
            genre = session["genre"]
            if "date" in session and session["date"] != "" and session["date"] != None:
                date = session["date"]
                movieList = dbmodel.getMovie(genre=genre,date=date)
            else:
                movieList = dbmodel.getMovie(genre=genre,)
            return render_template('Movie Details.html', title = 'Movie Details', movies = movieList, genreList = genreList, flag = flag, name = name)

        if "date" in session and session["date"] != "" and session["date"] != None:
            date = session["date"]
            if "genre" in session:
                genre = session["genre"]
                listFromDate = dbmodel.getMovie(genre=genre,date=date)
            else:
                listFromDate = dbmodel.getMovie(date=date)
            return render_template('Movie Details.html', title = 'Movie Details', movies = listFromDate, genreList = genreList, flag = flag, name = name)

    movies = dbmodel.getMovie(date="2021-04-01") # assume today is 2021-04-01
    session["date"] = "2021-04-01"
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
    session.pop('_flashes', None)
    if "logged_in" in session and session["logged_in"] == True and session['username'] == "admin":
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        name = None
        flash("User not found or not admin")
        return redirect(url_for('movieDetails'))
    members = dbmodel.getMemberTable()
    if request.method == 'POST':
        result = request.form
        memberTable = dbmodel.MemberTable
        email = result.get('email')
        creditCard = int(result.get('creditCard'))
        password = result.get ('password')
        new_member = memberTable(walletBalance=0,email=email,creditCard=creditCard,password=password)
        dbmodel.addMemberTableEntry(new_member)
        return render_template('memberList.html',all_member = members, name = name, flag = flag)
    else:
        return render_template('addUser.html',all_member = members, name = name, flag = flag)

@app.route('/memberList')
def member():
    if "logged_in" in session and session["logged_in"] == True and session['username'] == "admin":
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        flag = "0"
        name = None
        flash("User not found or not admin")
        return redirect(url_for('movieDetails'))
    members = dbmodel.getMemberTable()
    return render_template('memberList.html',all_member = members, name = name, flag = flag)

@app.route('/movieInfo', methods=['GET', 'POST'])
def movieInfo():
    print(session)
    if "logged_in" in session and session["logged_in"] == True:
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        name = None
        flag = "0"
    if request.method == 'POST':
        movieID = request.form.get("movie")
        session["movie"] = movieID
        return redirect(url_for('timeSelection'))
    movieId = session["movie"]
    movies = dbmodel.getMoviesTable(movieId)
    return render_template('MovieInfo.html',
                           title = 'Movie Info', movie = movies, flag = flag, name = name)

@app.route('/movieInfo/<int:movie_id>',methods = ['POST','GET'])
def showScreening(movie_id):
    movie = dbmodel.getAMovie(movie_id)
    if "logged_in" in session and session["logged_in"] == True and session['username'] == "admin":
        #IF ADMIN, SHOWS DIFFERENT INTERFACE, ALLOWS ADMIN TO UPDATE THE MOVIE DETAILS
        if request.method == 'POST':
            result = request.form
            movie.title = result.get('title')
            movie.blurb = result.get('blurb')
            movie.director = result.get('directors')
            movie.actorList = result.get('actors')
            movie.certificate = result.get('rating')
            dbmodel.db.session.commit()
            flash("Movie Updated...")
    return redirect(url_for('movieDetails'))

@app.route('/timeSelection',  methods=['GET', 'POST'])
def timeSelection():
    if "logged_in" in session and session["logged_in"] == True: # to check if user is online then hide the menu login and signup
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        name = None
        flag = "0"
    time = dbmodel.getATime(session["movie"],session["date"]) # get timetable by movieID and date
    all_bookings = dbmodel.getBookingTable()
    movie = movies = dbmodel.getMoviesTable(session["movie"])
    if request.method == 'POST':
        screeningID = request.form.get("movie")
        session["screeningID"] = screeningID # save screeningID
        if screeningID != None:
            return redirect(url_for('seats'))
    return render_template("timeSelection.html", movie = movie,flag = flag, name = name, time = time, bookings = all_bookings)

@app.route('/genre', methods = ['POST','GET'])
def genre():
    if "logged_in" in session and session["logged_in"] == True and session['username'] == "admin":
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        flag = "0"
        name = None
        flash("User not found or not admin")
        return redirect(url_for('movieDetails'))
    if request.method == 'POST':
        result = request.form
        genreTable = dbmodel.GenreTable
        genreDesc = result.get('genre')
        print(genreDesc)
        newGenre = genreTable(genreDesc = genreDesc)
        dbmodel.addGenre(newGenre)
    return render_template('genre.html',
                           genres = dbmodel.getGenres(), name = name, flag = flag)

@app.route('/addMovie')
def addMovie():
    if "logged_in" in session and session["logged_in"] == True and session['username'] == "admin":
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        flag = "0"
        name = None
        flash("User not found or not admin")
        return redirect(url_for('movieDetails'))
    return render_template('addMovie.html',
                           genres = dbmodel.getGenres(), name = name, flag = flag)

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
@app.route('/seats',methods = ['POST','GET'])
def seats():
    if "logged_in" in session and session["logged_in"] == True: # to check if user is online then hide the menu login and signup
        flag = "1" # when online
        name = dbmodel.getUserFromID(session["id"])
    else:
        flag = "0" # when offline
        name = None
    screeningTable = dbmodel.ScreeningTable
    screenTable = dbmodel.ScreenTable
    bookingTable = dbmodel.BookingTable
    paymentTable = dbmodel.PaymentTable

    screening_id = session["screeningID"] # from timeSelection.html
    screeningID = dbmodel.getScreeningID(screening_id) # 181th line in models.py, used for getting other data (seamNum,screenID,bookingTable)
    movie = dbmodel.getMovieInfoFromScreening(screening_id) #368th line in models.py
    screenID = dbmodel.getScreenID(int(dbmodel.getMovieInfoFromScreening(screening_id).movieID)) #to find rowID
    screen = dbmodel.getAScreen(screeningID.screenID) # for seatNum
    all_bookings = dbmodel.getBookingInfoForScreening(screening_id) # for checking booking table

    if request.method == 'POST':
        check = request.form.get("seats")
        child = request.form.get("child")
        adult = request.form.get("adult")
        elder = request.form.get("elder")
        result = request.form
        resultList = list(request.form.listvalues())
        resultList = resultList[0]
        resultList = resultList[0].split(",")
        if (int(child) + int(adult) + int(elder)) != len(resultList):
            flash("Need to select the number of seats correctly")
            return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],movie = movie, bookings=all_bookings, name = name, flag = flag)
        for row in resultList:
            if row == '':
                flash("You didn't select any seats")
                break
            rowID = dbmodel.rowIDFinder(screenID,int(row))
            print(rowID)
            new_booking = bookingTable(rowID=rowID,screeningID=screening_id,seatStatus=1)
            dbmodel.addBooking(new_booking) # works so it needs to be implemented after payment
            totalprice = int(child)*10 + int(adult)*15 + int(elder)*12
            new_totalprice = paymentTable(totalprice=totalprice) # count the total pirce
            dbmodel.addTotalprice(new_totalprice) # count the total pirce
            all_bookings = dbmodel.getBookingInfoForScreening(screening_id) # for checking booking table
            if "logged_in" in session and session["logged_in"] == True: # to check if user is online then hide the menu login and signup
                flag = "1" # when online
                name = dbmodel.getUserFromID(session["id"])
            else:
                flag = "0" # when offline
                name = None
            return redirect(url_for('payment'))
            
    return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],movie = movie, bookings=all_bookings, name = name, flag = flag)

@app.route('/payment',  methods=['GET', 'POST'])
def payment():
    if "logged_in" in session and session["logged_in"] == True: # to check if user is online then hide the menu login and signup
        name = dbmodel.getUserFromID(session["id"])
        flag = "1"
    else:
        name = None
        flag = "0"
    return render_template("paymentpage.html", flag = flag, name = name)
    

@app.route('/addFunds/<int:id>',methods = ['POST','GET'])
def addWallet(id):
    all_members = dbmodel.getMemberTable()
    user = dbmodel.getMember(id)
    name = dbmodel.getUserFromID(id)
    if request.method == 'POST':
        result = request.form
        balance = int(result.get('wallet'))
        wallet = int(user.walletBalance)
        wallet = balance + wallet
        user.walletBalance = str(wallet)
        dbmodel.db.session.commit()
        return render_template("addFunds.html",userOut = user, name = name, flag = "1")
    return render_template("addFunds.html",userOut = user, name = name, flag = "1")

@app.route('/addFunds/<int:id>/pay',methods = ['POST','GET'])
def payTickets(id):
    user = dbmodel.getMember(id)
    name = dbmodel.getUserFromID(id)
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
            return render_template("pay.html",userOut = user,messageOut = message, name=name,flag = "1")
        dbmodel.db.session.commit()
        return render_template("pay.html",userOut = user,messageOut = message, name=name, flag = "1")
    return render_template("pay.html",userOut = user, name=name, flag = "1")



@app.route('/signup', methods = ['GET', 'POST'])
def register():
    flag = "0"
    name = None
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
            return render_template('signup.html', flag = flag)
        else:
            card = result.get('card')
            print(type(card))
            pass1 = generate_password_hash(result.get('password'), method='sha256')
            pass2 = result.get('c_password')
            if(check_password_hash(pass1, pass2)):
                new_member = memberTable(email=ID,walletBalance=000.00,creditCard=card,password=pass1)
                dbmodel.addMember(new_member)
                flash("Successfully registered")
                return render_template('signin.html', flag = flag, name = name)
            else:
                flash("Password don't match")
                return render_template('signup.html', flag = flag, name = name)
    return render_template('signup.html', flag = flag, name = name)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    flag = "0"
    name = None
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
                return render_template('signin.html', flag = flag, name = name)
        else:
            flash("User not found")
            return render_template('signin.html', flag = flag, name = name)
    return render_template('signin.html' , flag = flag, name = name)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['id'] = None
    session['username'] = None
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
        admin = "1"
        print("is admin")
        return render_template('settings.html', admin = admin, name = current_user, flag = "1")
    else:
        admin = "0"
        print("is normal member")
        return render_template('settings.html', admin = admin, name = current_user, flag = "1")



@app.route('/addFunds')
def addFunds(member_id):
    return render_template('addFunds.html')

@app.route('/interface')
def showInterface():
    screeningTable = dbmodel.getScreeningTable()
    movieTable = dbmodel.getMoviesTable()
    screenTable = dbmodel.getScreenTable()
    return render_template("employeeInterface.html",
                            screeningTableOut = screeningTable,
                            movieTableOut = movieTable,
                            screenTableOut = screenTable)

#adding an interface for an employee
@app.route('/interface/<int:screeningID>',methods = ['POST','GET'])
def showSeating(screeningID):
    all_bookings = dbmodel.getBookingInfoForScreening(screeningID)
    bookingTable = dbmodel.BookingTable
    screening = dbmodel.getAScreening(int(screeningID))
    screenID = dbmodel.getScreenID(screening.movieID)
    screen = dbmodel.getAScreen(screening.screenID)
    movie = dbmodel.getAMovie(screening.movieID)
    if request.method == 'POST':
        resultList = list(request.form.listvalues())
        resultList = resultList[0]
        resultList = resultList[0].split(",")
        for row in resultList:
            rowID = dbmodel.rowIDFinder(screenID,int(row))
            new_booking = bookingTable(seatNumber=row,rowID=rowID,screeningID=screeningID,seatStatus=1,row="")
            dbmodel.addBooking(new_booking)
        redirect('/interface/<int:screeningID>')
        return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],bookings=all_bookings,screeningOut=screening,screeningIDOut = screeningID,movieOut=movie)
    return render_template("seatTest.html",screenOut = screen,rowDict = ['A','B','C','D','E','F','G'],bookings=all_bookings,screeningOut=screening,screeningIDOut = screeningID,movieOut=movie)
