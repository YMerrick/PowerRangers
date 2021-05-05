from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask
from app import app
from fpdf import FPDF
import re
import qrcode

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#This is only to print out the dir of objects in a pretty way
from pprint import pprint
app.secret_key = "secret key"

#Models class for database querying and limiting it to just methods
class Models():
    #Initialises the model class with the database and automaps the tables to classes
    def __init__(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'

        self.db = SQLAlchemy(app)

        Base = automap_base()
        Base.prepare(self.db.engine, reflect=True)
        self.MoviesTable     =   Base.classes.MoviesTable
        self.BookingTable    =   Base.classes.BookingTable
        self.CustomerTable   =   Base.classes.CustomerTable
        self.MemberTable     =   Base.classes.MemberTable
        self.PaymentTable    =   Base.classes.PaymentTable
        self.ScreeningTable  =   Base.classes.ScreeningTable
        self.ScreenTable     =   Base.classes.ScreenTable
        self.SeatTable       =   Base.classes.SeatTable
        self.TicketTable     =   Base.classes.TicketTable
        self.MovieGenreTable =   Base.classes.MovieGenreTable
        self.GenreTable      =   Base.classes.GenreTable
        self.CustomerType    =   Base.classes.CustomerType

    #Gets all the infromation from MoviesTable and dumps it in a list
    #If an id is passed then it returns the row corresponding to the id
    def getMoviesTable(self, movieID=None):
        #Trying to work out why query returns only one value from the database when there is 3
        #pprint(dir(self.db.session.query(self.MoviesTable)))
        #print(self.db.session.query(self.MoviesTable).count())
        if movieID!=None:
            return self.db.session.query(self.MoviesTable).filter_by(movieID=movieID).first()

        #returns all the data from the MoviesTable as an sqlalchemy object
        return self.db.session.query(self.MoviesTable).all()

    #Gets the movie record from the db and filters by the genre it is
    #Otherwise it returns all movies in the db
    def getMovieFromGenre(self,genre = None):
        genreQuery = self.db.session.query(self.MoviesTable).select_from(self.MoviesTable).join(self.MovieGenreTable).join(self.GenreTable).order_by(self.MoviesTable.title.asc())
        if genre == None:
            return genreQuery.all()
        else:
            return genreQuery.filter_by(genreDesc = genre).all()

    #Takes a movie title and returns the list of genres associated with it
    def getGenreForMovie(self,movieTitle):
        genreQuery = self.db.session.query(self.GenreTable).select_from(self.GenreTable).join(self.MovieGenreTable).join(self.MoviesTable).order_by(self.GenreTable.genreDesc.asc())
        queryList = genreQuery.filter_by(title = movieTitle).all()
        genreList = []
        for q in queryList:
            genreList.append(q.genreDesc)
        return genreList

    #Gets the information for a specific movie title
    def getMovieInfo(self, title):
        return self.db.session.query(self.MoviesTable).filter_by(title = title).first_or_404()

    #Gets all the genres in the db
    def getGenres(self):
        return self.db.session.query(self.GenreTable.genreDesc).order_by(self.GenreTable.genreDesc.asc()).all()

    #Gets the screening info for a bookingID and returns the automap object
    #This method also gives the screen its showing on
    #Returns the title, date, time and screen name as a tuple
    def getScreeningInfoForBooking(self,bookingID):
        return (
                self.db.session.query(self.MoviesTable.title,self.ScreenTable.screenName,self.ScreeningTable.time,self.ScreeningTable.date)
                .select_from(self.BookingTable)
                .filter_by(bookingID = bookingID)
                .join(self.ScreeningTable)
                .join(self.MoviesTable)
                .join(self.ScreenTable)
        )

    #Gets the seat row and returns the automap object
    def getSeatInfoForBooking(self,bookingId):
        return (
                self.db.session.query(self.SeatTable.rowNumber, self.BookingTable.seatNumber)
                .select_from(self.BookingTable)
                .filter_by(bookingID = bookingId)
                .join(self.SeatTable)
                .subquery()
        )

    #Gets the booking information from the ticket ID
    def getBookingInfoForTicket(self,ticketId):
        ticketInfo = (
            self.db.session.query(self.MoviesTable.title,self.ScreenTable.screenName,self.ScreeningTable.time,self.ScreeningTable.date,self.SeatTable.rowNumber, self.SeatTable.seatCount, self.TicketTable.ticketID)
            .select_from(self.TicketTable).filter_by(ticketID = ticketId)
            .join(self.ScreenTable, self.ScreeningTable.screenID == self.ScreenTable.screenID)
            .join(self.SeatTable, self.BookingTable.rowID == self.SeatTable.rowID)
            .join(self.MoviesTable, self.ScreeningTable.movieID == self.MoviesTable.movieID)
            .join(self.BookingTable, self.TicketTable.bookingID == self.BookingTable.bookingID)
            .join(self.ScreeningTable, self.BookingTable.screeningID == self.ScreeningTable.screeningID)
        )
        return ticketInfo.first()

    #Gets the ticket information from the customer ID
    def getTicketInfo(self,ticketId):
        pass

    def getBookingTable(self):
        return self.db.session.query(self.BookingTable).all()

    def getCustomerTable(self):
        return self.db.session.query(self.CustomerTable).all()

    def getMemberTable(self, memberID = None):
        if memberID!=None:
            return self.db.session.query(self.MemberTable).filter_by(memberID=memberID).first()
        return self.db.session.query(self.MemberTable).all()

    def getPaymentTable(self):
        return self.db.session.query(self.PaymentTable).all()

    def getScreeningTable(self):
        return self.db.session.query(self.ScreeningTable).all()

    def getScreenTable(self):
        return self.db.session.query(self.ScreenTable).all()

    def getSeatTable(self):
        return self.db.session.query(self.SeatTable).all()

    def getTicketTable(self):
        return self.db.session.query(self.TicketTable).all()

    #Adds a genre taken as an automapped class of the GenreTable
    def addGenre(self,genreIn):
        self.db.session.add(genreIn)
        self.db.session.commit()
        return True

    #returns True if genres have been added to movie and false otherwise
    def addGenreForMovie(self,genres,movieTitle):
        if type(genres) == type([]):
            for genre in genres:
                genreTable = self.MovieGenreTable
                genreId = self.db.session.query(self.GenreTable.genreID).filter_by(genreDesc = genre).first().genreID
                movieId = self.db.session.query(self.MoviesTable.movieID).filter_by(title = movieTitle).first().movieID
                newGenreForMovie = genreTable(movieID=movieId,genreID=genreId)
                self.db.session.add(newGenreForMovie)
            self.db.session.commit()
            return True
        return False

    def addMoviesTableEntry(self,movieIn,genre):
        self.db.session.add(movieIn)
        self.db.session.commit()
        self.addGenreForMovie(genre,movieIn.title)
        return 0

    def getTitle(self, title = "Demon Slayer: Kimetsu no Yaiba the Movie: Mugen Train"):
        title = self.db.session.query(self.MoviesTable).filter_by(title=title)
        return title.one().title

    #getting screening ID by movie_id
    def getScreenID(self,movie_id):
        screenTable = self.ScreenTable
        screeningTable = self.ScreeningTable
        screenID = self.db.session.query(screeningTable.screenID).filter_by(movieID=movie_id).first().screenID
        return screenID


    #getting screen by screenID

    #get a time table by movie-id and date
    def getATime(self,movie_id,date):
        screeningTable = (self.ScreeningTable.screenID,self.ScreeningTable.screeningID,self.ScreeningTable.movieID,self.ScreeningTable.date,self.ScreeningTable.time)
        timeTable = self.db.session.query(
            self.ScreeningTable.screenID,
            self.ScreeningTable.screeningID,
            self.ScreeningTable.movieID,
            self.ScreeningTable.date,
            self.ScreeningTable.time,
            self.ScreenTable.screenName
        ).select_from(self.ScreeningTable).filter_by(movieID=movie_id,date=date).join(self.ScreenTable, self.ScreeningTable.screenID == self.ScreenTable.screenID).all()
        return timeTable

    #get a ScreeningTable screeningID
    def getScreeningID(self,screeningID):
        screeningTable = self.ScreeningTable
        screeningID = self.db.session.query(screeningTable).filter_by(screeningID=screeningID).first()
        return screeningID
        
    #get a ScreeningTable screeningID
    def getBookingbyScreeningID(self,screeningID):
        screening = self.db.session.query(self.BookingTable).filter_by(screeningID=screeningID).all()
        return screening

        #getting screen by screenID

    def getAScreen(self,screenID):
        screenTable = self.ScreenTable
        screen = self.db.session.query(screenTable).get(screenID)
        return screen

    #getting a movie by id
    def getAMovie(self,movieID):
        movieTable = self.MoviesTable
        movie = self.db.session.query(movieTable).get(movieID)
        return movie

    #getting a screening by screeningID
    def getAScreening(self,screeningID):
        screeningTable = self.ScreeningTable
        screening = self.db.session.query(screeningTable).get(screeningID)
        return screening

    #getting tickets
    def getTickets(self,memberIDIn):
        ticketsTable = self.TicketTable
        tickets = self.db.session.query(ticketsTable).filter_by(memberID=str(memberIDIn)).all()
        return tickets

    #adding members into member
    def addMemberTableEntry(self,memberIn):
        memberTable = self.MemberTable
        self.db.session.add(memberIn)
        self.db.session.commit()
        return 0

    def getMember(self,memberID):
        memberTable = self.MemberTable
        member = self.db.session.query(memberTable).get(memberID)
        return member

    #Returns the screening dates in months
    #Takes
    def dateExchange(self,dates):

        def monthToNum(numMonth):
            return {
                    '01' : 'JAN',
                    '02' : 'FEB',
                    '03' : 'MAR',
                    '04' : 'APR',
                    '05' : 'MAY',
                    '06' : 'JUN',
                    '07' : 'JUL',
                    '08' : 'AUG',
                    '09' : 'SEP',
                    '10' : 'OCT',
                    '11' : 'NOV',
                    '12' : 'DEC'
            }[numMonth]

        dateList = []
        for d in dates:
            date = d.date.split('-')
            month = monthToNum(date[1])
            x = (d.time,month + date[2])
            dateList.append(x)
        return dateList

    #times that a movie is going to be screening at
    #Takes a movie title and then outputs all screenings
    def getScreeningTimeForMovie(self,title):
        screeningInfo =  (
            self.db.session.query(self.ScreeningTable.time, self.ScreeningTable.date)
            .select_from(self.ScreeningTable)
            .join(self.MoviesTable)
            .filter_by(title = title)
        )
        screeningList = self.dateExchange(screeningInfo.all())
        return screeningList

    #Returns movie query from genres
    def getMoviesFromGenre(self,query,genre):
        genreQuery = (
            query
            .join(self.MovieGenreTable)
            .join(self.GenreTable)
            .filter_by(genreDesc = genre)
        )
        return genreQuery

    #return movies from the date that it is screening
    #Returns all movies relating to the date asked for
    def getMovieFromDate(self,query,date):
        movieInfo = query.join(self.ScreeningTable).filter_by(date = date)
        return movieInfo

    #Returns all movies filtered by date and genre if either are present or not
    def getMovie(self,date=None,genre=None):
        movieInfo = (
            self.db.session.query(self.MoviesTable)
            .select_from(self.MoviesTable)
        )
        if genre != None:
            movieInfo = self.getMoviesFromGenre(movieInfo,genre)
        if date != None:
            movieInfo = self.getMovieFromDate(movieInfo,date)
        return movieInfo.order_by(self.MoviesTable.title.asc()).all()

    def set_password(self, password):
        self.password = generate_password_hash(password,method='sha256')

    def addMember(self,memberIn):
        self.db.session.add(memberIn)
        self.db.session.commit()
        return True

    def addTotalprice(self,totalPrice):
        self.db.session.add(totalPrice)
        self.db.session.commit()
        return True

    def getPriceFromPaymentID(self,paymentID):
        price = (
            self.db.session.query(self.PaymentTable.totalprice)
            .filter_by(paymentID = paymentID)
        )
        return price.first()
    
    def getPayment(self,paymentID):
        payment = (
            self.db.session.query(self.PaymentTable).get(paymentID)
        )
        return payment

    def getMemberfromPaymentID(self,paymentId):
        memberID = self.db.session.query(self.PaymentTable.memberID).filter_by(paymentID = paymentID)
        member = self.db.session.query(self.MemberTable).filter_by(memberID = memberID).first()
        return member

    def getPaymentListfromPMemberID(self,memberID):
        paymentList = self.db.session.query(self.PaymentTable.memberID).filter_by(memberID = memberID).all()   
        return paymentList

    def updatePayment(self,paymentID,paymentMethod=None,chargeID=None):
        paymentRecord = self.getPayment(paymentId)
        paymentRecord.paymentMethod = paymentMethod
        paymentRecord.chargeID = chargeId
        self.db.session.commit()

    def getPriceOfTickets(self):
        prices = (
            self.db.session.query(self.CustomerType)
        ).all()
        priceDict = {
            "Under16":int(prices[0].price),
            "Adult":int(prices[1].price),
            "Senior":int(prices[2].price)
        }
        return priceDict

    def getUserFromID(self, memberID):
        member = self.db.session.query(self.MemberTable).filter_by(memberID = memberID).first()
        return member

    #checks if userIn's email/credit card exist in the database, if exists, return false
    def getUserFromEmail(self, emailIn):
        member = self.db.session.query(self.MemberTable).filter_by(email = emailIn).first()
        return member

    #Method to create the pdf for a ticket
    def makeTicketPdf(self,ticketId):
        location = 'app/static/'
        file = FPDF(orientation = 'L', format = (74,105))

        qr = qrcode.QRCode(
            version=1,
            box_size=4,
            border=4,
        )
        qr.add_data(ticketId)
        qr.make(fit=True)

        file.open()
        file.add_page()

        file.set_font('Times')
        file.cell(file.epw,file.font_size,txt= 'Ticket',ln=file.font_size)

        file.set_font('Courier',size= 10)
        ticketInfo = self.getBookingInfoForTicket(ticketId)
        print(ticketInfo)
        qrCodeImg = qr.make_image(fill_color="black", back_color="white")
        file.cell(17,file.font_size,txt= 'Title: ')
        file.multi_cell(0,file.font_size,txt= ticketInfo.title,ln=1,max_line_height=file.font_size)
        file.cell(file.epw,file.font_size,txt= 'Screen: '+ticketInfo.screenName,ln=1)
        file.cell(17,file.font_size,txt='Time: ')
        file.cell(0,file.font_size,txt=ticketInfo.time,ln=1)
        file.cell(17,file.font_size,txt='Date: ')
        file.cell(0,file.font_size,txt=ticketInfo.date,ln=1)
        file.cell(17,file.font_size,txt='Row: ')
        file.cell(0,file.font_size,txt=str(ticketInfo.rowNumber),ln=1)
        file.cell(17,file.font_size,txt='Seat: ')
        file.cell(0,file.font_size,txt=str(ticketInfo.seatCount),ln=1)
        file.image(qrCodeImg.get_image(),x=60,y=32)

        file.output(name = location+'tickets/' + str(ticketId)+'.pdf')
        file.close()

    def updateMovieRecord(self,movieId):
        self.db.session
        pass

    #find the seat number
    def rowIDFinder(self,screenIDIn,row):
        if(screenIDIn == 1):
            return 0+row
        elif(screenIDIn == 2):
            return 60+row
        elif(screenIDIn == 3):
            return 108+row

    #add booking to the database
    def addBooking(self,bookingIn):
        memberTable = self.BookingTable
        self.db.session.add(bookingIn)
        self.db.session.commit()
        pass

    def getRowForScreening(self,screenId):
        row = (
            self.db.session.query(self.SeatTable)
            .select_from(self.SeatTable).filter_by(screenID = screenId)
            .join(self.ScreenTable, self.SeatTable.screenID == self.ScreenTable.screenID)
            .join(self.ScreeningTable ,self.ScreenTable.screenID == self.ScreenTable.screenID)
        )
        return row.all()

    def getBookingInfoForScreening(self,screeningID):
        bookedSeats = (
            self.db.session.query(self.BookingTable,self.SeatTable.rowNumber,self.SeatTable.seatCount)
            .select_from(self.BookingTable)
            .filter_by(screeningID=screeningID)
            .join(self.SeatTable)
        )
        return bookedSeats.all()

    def getMovieInfoFromScreening(self,screeningId):
        movieInfo = (
            self.db.session.query(self.MoviesTable)
            .select_from(self.ScreeningTable)
            .filter_by(screeningID = screeningId)
            .join(self.MoviesTable)
        )
        return movieInfo.first()

