from flask import render_template
from flask import Flask
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
MoviesTable = Base.classes.MoviesTable


@app.route('/')
def index():
    movies = db.session.query(MoviesTable).all()
    return render_template('movieList.html',
                           title='Movie List', all_movies = movies)