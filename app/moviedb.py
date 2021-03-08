import sqlite3

con = sqlite3.connect("movie.db")
print("Database opened successfully")

con.close()