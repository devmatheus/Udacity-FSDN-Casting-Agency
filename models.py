import os
from datetime import date
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_HOST'),
    os.environ.get('DB_PORT'),
    os.environ.get('DB_NAME')
)
db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    john = Actor(
        name='John Doe',
        bio='John Doe is an actor.'
    )
    john.insert()

    jane = Actor(
        name='Jane Doe',
        bio='Jane Doe is an actor.'
    )
    jane.insert()

    movie1 = Movie(
        title='Movie 1',
        release_date=date.today()
    )
    movie1.insert()
    movie1.actors.append(john)

    movie2 = Movie(
        title='Movie 2',
        release_date=date.today()
    )
    movie2.insert()
    movie2.actors.append(john)
    movie2.actors.append(jane)


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
