from datetime import date
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
# TODO: Use .env file to store database path
database_path = "postgresql://{}/{}".format('localhost:5432', 'capstone')
db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # TODO: Add some data to the database

# Actors
class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bio = Column(String, nullable=True)

    movies = db.relationship('Movie', secondary='movie_actor', backref=db.backref('actors', lazy=True))

# Movies
class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(date, nullable=True)

    actors = db.relationship('Actor', secondary='movie_actor', backref=db.backref('movies', lazy=True))

    @property
    def start_time_formatted(self):
        return self.start_time.strftime('%d %B %Y %H:%M')
