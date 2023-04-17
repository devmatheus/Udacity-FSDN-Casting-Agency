import os
import requests
from flask import (
    Flask,
    render_template,
    request,
    abort,
    jsonify,
    session,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from urllib.parse import urlencode

from models import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
  app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
  setup_db(app)

  db_drop_and_create_all()
  
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response
  
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": "unauthorized"
      }), 401

  @app.errorhandler(403)
  def forbidden(error):
      return jsonify({
          "success": False,
          "error": 403,
          "message": "forbidden"
      }), 403

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
      }), 500
  
  @app.errorhandler(AuthError)
  def auth_error(error):
      if not request.path.startswith('/api'):
          return redirect(url_for('login'))
      
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error
      }), error.status_code

  return app

APP = create_app()

#region Interface Endpoints
@APP.route('/')
@requires_auth()
def index(payload):
    '''
    Renders the home page

    Returns:
        HTML: The home page
    '''
    return render_template('pages/home.html', token = session.get('jwt_token'), permissions = payload['permissions'])

@APP.route('/actors')
@requires_auth()
def actors(payload):
    '''
    Renders the actors page

    Returns:
        HTML: The actors page
    '''
    return render_template('pages/actors.html', permissions = payload['permissions'])

@APP.route('/movies')
@requires_auth()
def movies(payload):
    '''
    Renders the movies page

    Returns:
        HTML: The movies page
    '''
    return render_template('pages/movies.html', permissions = payload['permissions'])

@APP.route('/movies/create')
@requires_auth('create:movies')
def create_movie(payload):
    '''
    Renders the movie form page

    Returns:
        HTML: The movie form page
    '''
    actors = Actor.query.order_by(Actor.name).all()
    return render_template('forms/movie.html', action='Add', actors=actors, permissions = payload['permissions'])

@APP.route('/actors/create')
@requires_auth('create:actors')
def create_actor(payload):
    '''
    Renders the actor form page

    Returns:
        HTML: The actor form page
    '''
    return render_template('forms/actor.html', action='Add', permissions = payload['permissions'])

@APP.route('/movies/<int:movie_id>/edit')
@requires_auth('patch:movies')
def edit_movie(payload, movie_id):
    '''
    Renders the movie form page

    Parameters:
        movie_id (int): The movie id
    
    Returns:
        HTML: The movie form page
    '''
    actors = Actor.query.order_by(Actor.name).all()
    return render_template('forms/movie.html', action='Edit', actors=actors, permissions = payload['permissions'])

@APP.route('/actors/<int:actor_id>/edit')
@requires_auth('patch:actors')
def edit_actor(payload, actor_id):
    '''
    Renders the actor form page

    Parameters:
        actor_id (int): The actor id

    Parameters:
        actor_id (int): The actor id
    '''
    return render_template('forms/actor.html', action='Edit', permissions = payload['permissions'])

@APP.route('/login')
def login():
    '''
    Redirects the user to the Auth0 login page

    Returns:
        Redirect: The Auth0 login page
    '''
    base_url = f'https://{os.environ.get("AUTH0_DOMAIN")}/authorize'
    params = {
        'audience': os.environ.get('AUTH0_API_AUDIENCE'),
        'response_type': 'code',
        'client_id': os.environ.get('AUTH0_CLIENT_ID'),
        'redirect_uri': os.environ.get('AUTH0_CALLBACK_URL'),
        'scope': 'openid profile email'
    }

    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)

@APP.route('/logout')
def logout():
    '''
    Logs the user out of the application

    Returns:
        Redirect: The Auth0 logout page
    '''
    session.clear()

    return redirect(f'https://{os.environ.get("AUTH0_DOMAIN")}/v2/logout?client_id={os.environ.get("AUTH0_CLIENT_ID")}&returnTo={os.environ.get("AUTH0_LOGOUT_CALLBACK_URL")}')

@APP.route('/auth0-callback')
def callback():
    '''
    Handles the Auth0 callback

    Returns:
        Redirect: The home page
    '''
    code = request.args.get('code')
    token_url = f'https://{os.environ.get("AUTH0_DOMAIN")}/oauth/token'
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': os.environ.get('AUTH0_CLIENT_ID'),
        'client_secret': os.environ.get('AUTH0_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': os.environ.get('AUTH0_CALLBACK_URL'),
        'audience': os.environ.get('AUTH0_API_AUDIENCE')
    }
    token_headers = {'Content-Type': 'application/json'}

    token_response = requests.post(token_url, json=token_payload, headers=token_headers)
    token_response.raise_for_status()
    tokens = token_response.json()
    
    session['jwt_token'] = tokens['access_token']

    return redirect(url_for('index'))
#endregion

#region API Endpoints
@APP.route('/api/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    '''
    Gets a list of actors

    Returns:
        JSON: A list of actors
    '''
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    actors = Actor.query.paginate(page=page, per_page=page_size)

    if actors.total == 0:
        abort(404)

    return jsonify({
        'success': True,
        'actors': [actor.format() for actor in actors.items],
        'total_actors': actors.total,
        'current_page': actors.page,
        'total_pages': actors.pages
    })

@APP.route('/api/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    '''
    Gets a list of movies

    Returns:
        JSON: A list of movies
    '''
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    movies = Movie.query.paginate(page=page, per_page=page_size)
    if movies.total == 0:
        abort(404)

    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies.items],
        'total_movies': movies.total,
        'current_page': movies.page,
        'total_pages': movies.pages
    })

@APP.route('/api/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(payload, actor_id):
    '''
    Gets an actor by id

    Parameters:
        actor_id (int): The actor id

    Returns:
        JSON: The actor
    '''
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    return jsonify({
        'success': True,
        'data': actor.format()
    })

@APP.route('/api/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(payload, movie_id):
    '''
    Gets a movie by id

    Parameters:
        movie_id (int): The movie id

    Returns:
        JSON: The movie
    '''
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    return jsonify({
        'success': True,
        'data': movie.format()
    })

@APP.route('/api/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    '''
    Deletes an actor by id

    Parameters:
        actor_id (int): The actor id

    Returns:
        JSON: The deleted actor id
    '''
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    actor.delete()
    return jsonify({
        'success': True,
        'delete': actor_id
    })

@APP.route('/api/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    '''
    Deletes a movie by id

    Parameters:
        movie_id (int): The movie id

    Returns:
        JSON: The deleted movie id
    '''
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    movie.delete()
    return jsonify({
        'success': True,
        'delete': movie_id
    })

@APP.route('/api/actors', methods=['POST'])
@requires_auth('create:actors')
def create_actor(payload):
    '''
    Creates an actor

    Returns:
        JSON: Success
    '''
    actor = Actor(
        name=request.json.get('name'),
        bio=request.json.get('bio')
    )
    actor.insert()
    return jsonify({
        'success': True
    })

@APP.route('/api/movies', methods=['POST'])
@requires_auth('create:movies')
def create_movie(payload):
    '''
    Creates a movie

    Returns:
        JSON: Success
    '''
    movie = Movie(
        title=request.json.get('title'),
        release_date=request.json.get('release_date')
    )
    movie.insert()
    for actor_id in request.json.get('actors'):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is not None:
            movie.actors.append(actor)
    movie.update()
    return jsonify({
        'success': True
    })

@APP.route('/api/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    '''
    Updates an actor by id

    Parameters:
        actor_id (int): The actor id

    Returns:
        JSON: Success
    '''
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    actor.name = request.json.get('name', actor.name)
    actor.bio = request.json.get('bio', actor.bio)
    actor.update()
    return jsonify({
        'success': True
    })

@APP.route('/api/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    '''
    Updates a movie by id

    Parameters:
        movie_id (int): The movie id

    Returns:
        JSON: Success
    '''
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    movie.title = request.json.get('title', movie.title)
    movie.release_date = request.json.get('release_date', movie.release_date)
    if 'actors' in request.json:
        movie.actors = []
        for actor_id in request.json.get('actors'):
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is not None:
                movie.actors.append(actor)
    movie.update()
    return jsonify({
        'success': True
    })
#endregion

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
    