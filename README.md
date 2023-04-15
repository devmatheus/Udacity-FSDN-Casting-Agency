# Udacity Full Stack Web Development Nanodegree - Final Project: Casting Agency

## Introduction

This project is the final project for the Udacity Full Stack Web Development Nanodegree. It is a Casting Agency Project that allows users to view and add actors and movies to the database. The API is built using Flask and SQLAlchemy.

## Authors
- [**Matheus Machado**](matheusdev@me.com);

## Getting Started

### Installing Dependencies

You can install the dependencies using the following command:

```sh
$ pip install -r requirements.txt
```

### Running the server locally

To run the server, execute:

```sh
$ python app.py
```

### Database Setup

Create a copy of the `.env.example` file and rename it to `.env`. Then, fill in the environment variables with your own values.

```sh
$ cp .env.example .env
```

## API Reference

### Getting Started

- Base URL: This app can be run locally and it is hosted at the default, http://127.0.0.1:8080
- Authentication: This application uses Auth0 for authentication. The following roles are available:
  - Administrator: Can view actors and movies, add actors and movies, and delete actors and movies.
  - Producer: Can view actors and movies and add actors and movies.


### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints

#### GET /actors

- General:
  - Returns a list of actors, success value, total number of actors, and total number of pages.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:8080/api/actors?page=1`

```json
{
  "actors": [
    {
      "id": 1, 
      "name": "John Doe",
      "bio": "John Doe is an actor."
    }
  ], 
  "current_page": 1, 
  "success": true, 
  "total_actors": 1, 
  "total_pages": 1
}
```

#### GET /movies

- General:
  - Returns a list of movies, success value, total number of movies, and total number of pages.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:8080/api/movies?page=1`

```json
{
  "movies": [
    {
      "actors": [
        {
          "id": 1, 
          "name": "John Doe",
          "bio": "John Doe is an actor." 
        }, 
        {
          "id": 2, 
          "name": "Jane Doe",
          "bio": "Jane Doe is an actress." 
        }
      ], 
      "id": 1, 
      "release_date": "2023-04-15", 
      "release_date_formatted": "15 April 2023", 
      "title": "Test Movie"
    }
  ], 
  "current_page": 1, 
  "success": true, 
  "total_movies": 1, 
  "total_pages": 1
}
```

#### POST /actors

- General:
  - Creates a new actor using the submitted name, bio, and age. Returns success value.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "bio": "John Doe is an actor."}' http://127.0.0.1:8080/api/actors`

```json
{
  "success": true
}
```

#### POST /movies

- General:
  - Creates a new movie using the submitted title, release date, and actors. Returns success value.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Test Movie", "release_date": "2023-04-15", "actors": [1, 2]}' http://127.0.0.1:8080/api/movies`

```json
{
  "success": true
}
```

#### PATCH /actors/<int:actor_id>

- General:
  - Updates the actor with the given ID using the submitted name, and bio. Returns success value.
- Sample: `curl -X PATCH -H "Content-Type: application/json" -d '{"name": "John Doe"}' http://127.0.0.1:8080/api/actors/1`

```json
{
  "success": true
}
```

#### PATCH /movies/<int:movie_id>

- General:
  - Updates the movie with the given ID using the submitted title, release date, and actors. Returns success value.
- Sample: `curl -X PATCH -H "Content-Type: application/json" -d '{"title": "Test Movie"}' http://127.0.0.1:8080/api/movies/1`

```json
{
  "success": true
}
```

#### DELETE /actors/<int:actor_id>

- General:
  - Deletes the actor with the given ID. Returns success value, and the ID of the deleted actor.
- Sample: `curl -X DELETE http://127.0.0.1:8080/api/actors/1`

```json
{
  "deleted": 1, 
  "success": true
}
```

#### DELETE /movies/<int:movie_id>

- General:
  - Deletes the movie with the given ID. Returns success value, and the ID of the deleted movie.
- Sample: `curl -X DELETE http://127.0.0.1:8080/api/movies/1`

```json
{
  "deleted": 1, 
  "success": true
}
```

### Testing

You can setup a new database using the .env file, example:

```
DATABASE_STAGING_HOST=localhost
DATABASE_STAGING_PORT=5432
DATABASE_STAGING_NAME=capstone
DATABASE_STAGING_USER=postgres
DATABASE_STAGING_PASSWORD=postgres
```

Then run the following commands:

```sh
$ python test_app.py
```
