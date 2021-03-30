from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask
from app import app
from pprint import pprint



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

    #Gets all the infromation from MoviesTable and dumps it in a list
    def getMoviesTable(self):
        #Trying to work out why query returns only one value from the database when there is 3
        pprint(dir(self.db.session.query(self.MoviesTable)))
        print(self.db.session.query(self.MoviesTable).count())
        
        #returns all the data from the MoviesTable as an sqlalchemy object
        return self.db.session.query(self.MoviesTable).all()
    
    def getBookingTable(self):
        pass

    def getCustomerTable(self):
        pass

    def getMemberTable(self):
        pass

    def getPaymentTable(self):
        pass

    def getScreeningTable(self):
        pass

    def getScreenTable(self):
        pass

    def getSeatTable(self):
        pass

    def TicketTable(self):
        pass