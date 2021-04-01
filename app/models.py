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
    def getMovieFromGenre(self,genre = None):
        genreQuery = self.db.session.query(self.MoviesTable).select_from(self.MoviesTable).join(self.MovieGenreTable).join(self.GenreTable).order_by(self.MoviesTable.title.asc())
        if genre == None:
            return genreQuery.all()
        else:
            return genreQuery.filter_by(genreDesc = genre).all()

    def getMovieInfo(self, title):
        return self.db.session.query(self.MoviesTable).filter_by(title = title).first_or_404()
    
    def getGenres(self):
        return self.db.session.query(self.GenreTable.genreDesc).order_by(self.GenreTable.genreDesc.asc()).all()

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

    def addMoviesTableEntry(self,movieIn):
        self.db.session.add(movieIn)
        self.db.session.commit()
        return 0
    
    def getTitle(self, title = "Demon Slayer: Kimetsu no Yaiba the Movie: Mugen Train"):
        title = self.db.session.query(self.MoviesTable).filter_by(title=title)
        return title.one().title
