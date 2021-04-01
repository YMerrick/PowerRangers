from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask
from app import app
#This is only to print out the dir of objects in a pretty way
from pprint import pprint


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

    #Gets all the infromation from MoviesTable and dumps it in a list
    def getMoviesTable(self):
        #Trying to work out why query returns only one value from the database when there is 3
        #pprint(dir(self.db.session.query(self.MoviesTable)))
        #print(self.db.session.query(self.MoviesTable).count())
        
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
    def getScreeningInfoForBooking(self,bookingID):
        return self.db.session.query(self.MoviesTable.title,self.ScreenTable.screenName,self.ScreeningTable.time,self.ScreeningTable.date).select_from(self.BookingTable).join(self.ScreeningTable).join(self.MoviesTable).join(self.ScreenTable)

    #Gets the seat row and returns the automap object
    def getSeatInfo(self):
        pass

    #Gets the booking information from a screening and seat number and row
    def getBookingInfo(self):
        pass

    #Gets the ticket information from the customer ID 
    def getTicketInfo(self):
        
        pass

    def getBookingTable(self):
        return self.db.session.query(self.BookingTable).all()

    def getCustomerTable(self):
        return self.db.session.query(self.CustomerTable).all()

    def getMemberTable(self):
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
