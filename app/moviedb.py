import sqlite3

con = sqlite3.connect("movie.db")
print("Database opened successfully")

print("Would you like to make the tables? enter 1 to confirm: \n")
x = int(input())
if x == 1:
    #con.execute("create table ScreenTable (screenID INTEGER PRIMARY KEY AUTOINCREMENT, seatNum INTEGER NOT NULL)")
    #con.execute("create table CustomerType (customerTypeID INTEGER PRIMARY KEY AUTOINCREMENT, ageGroup INTEGER NOT NULL, price DECIMAL(4,2) NOT NULL)")
    #con.execute("create table MemberTable (memberID INTEGER PRIMARY KEY AUTOINCREMENT, walletBalance DECIMAL(5,2) NOT NULL, email TEXT NOT NULL, creditCard NUMERIC(16) UNIQUE)")
    #con.execute("create table MoviesTable (movieID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, blurb MEDIUMTEXT, certificate TEXT, genre TEXT, director TEXT, actorList TEXT)")
    #con.execute("create table ScreeningTable (screeningID INTEGER PRIMARY KEY AUTOINCREMENT, screenID INTEGER FORIEGN KEY REFERENCES ScreenTable(screenID), movieID INTEGER FORIEGN KEY REFERENCES MoviesTable(movieID), date TEXT NOT NULL, time TEXT NOT NULL)")
    #con.execute("create table SeatTable (rowNumber INTEGER PRIMARY KEY AUTOINCREMENT, seatCount INTEGER NOT NULL, screenID INTEGER FORIEGN KEY REFERENCES ScreenTable(screenID))")
    #con.execute("create table BookingTable (bookingID INTEGER PRIMARY KEY AUTOINCREMENT, seatNumber INTEGER NOT NULL, rowNumber INTEGER FORIEGN KEY REFERENCES SeatTable(rowNumber), screeningID INTEGER FORIEGN KEY REFERENCES ScreeningTable(screeningID), seatStatus BOOLEAN NOT NULL)")
    #con.execute("create table PaymentTable (paymentID INTEGER PRIMARY KEY AUTOINCREMENT, paymentMethod TEXT NOT NULL, customerTypeID INTEGER FORIEGN KEY REFERENCES CustomerType(customerTypeID))")
    #con.execute("create table TicketTable (ticketID INTEGER PRIMARY KEY AUTOINCREMENT, bookingID INTEGER FORIEGN KEY REFERENCES BookingTable(bookingID), customerTypeID INTEGER FORIEGN KEY REFERENCES CustomerType(customerTypeID))")
    #con.execute("create table CustomerTable (customerID INTEGER PRIMARY KEY AUTOINCREMENT, ticketID INTEGER FORIEGN KEY REFERENCES TicketTable(ticketID), paymentID INTEGER FORIEGN KEY REFERENCES PaymentTable(paymentID), memberID INTEGER FORIEGN KEY REFERENCES MemberTable(memberID))")
    pass

con.close()