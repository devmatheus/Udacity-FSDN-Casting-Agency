import os
from dotenv import load_dotenv
from datetime import date
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

project_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get('DATABASE_USER'),
    os.environ.get('DATABASE_PASSWORD'),
    os.environ.get('DATABASE_HOST'),
    os.environ.get('DATABASE_PORT'),
    os.environ.get('DATABASE_NAME')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    # db.drop_all()
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

movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

# Actors
class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bio = Column(String, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio
        }
    
# Movies
class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date, nullable=True)

    actors = db.relationship('Actor', secondary='movie_actor', backref=db.backref('movies', lazy=True))

    @property
    def release_date_formatted(self):
        return self.release_date.strftime('%d %B %Y')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'release_date_formatted': self.release_date_formatted,
            'actors': [actor.format() for actor in self.actors]
        }
