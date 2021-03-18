from flask import render_template
from flask import Flask
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

BookingTable = Base.classes.BookingTable
CustomerTypeTable = Base.classes.CustomerType
CustomerTable = Base.classes.CustomerTable
PaymentTable = Base.classes.PaymentTable
BookingTable = Base.classes.BookingTable
TicketsTable = Base.classes.TicketTable
ScreeningTable = Base.classes.ScreeningTable
MoviesTable = Base.classes.MoviesTable
SeatTable = Base.classes.SeatTable

@app.route('/')
def index():
    results = db.session.query(CustomerTypeTable).all()
    
    user = {'name': 'Power-Rangers'}
    return render_template('index.html',
                           title='Home',
                           user=user,
                            test_result = results)


@app.route('/tickets')
def ticketPage():
    ticket = db.session.query(TicketsTable).get(0)
    booking = db.session.query(BookingTable).get(ticket.bookingID)
    customer = db.session.query(CustomerTable).filter_by(ticketID = ticket.ticketID).first()
    customerType = db.session.query(CustomerTypeTable).get(ticket.customerTypeID)
    payment = db.session.query(PaymentTable).get(customer.paymentID)
    screen = db.session.query(ScreeningTable).get(booking.screeningID)
    movie = db.session.query(MoviesTable).get(screen.movieID)
    seat = db.session.query(SeatTable).get(booking.rowID)

    return render_template('tickets.html',
                            testTicket = ticket,
                            testBooking = booking,
                            testCustomer = customer,
                            testCustomerType = customerType,
                            testScreen = screen,
                            testPayment = payment,
                            testMovie = movie,
                            testSeat = seat)