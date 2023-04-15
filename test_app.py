import os
import unittest
import json

from app import create_app
from models import setup_db

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        os.environ['TESTING'] = 'True'
        os.environ['DATABASE_HOST'] = os.environ.get('DATABASE_STAGING_HOST')
        os.environ['DATABASE_PORT'] = os.environ.get('DATABASE_STAGING_PORT')
        os.environ['DATABASE_NAME'] = os.environ.get('DATABASE_STAGING_NAME')
        os.environ['DATABASE_USER'] = os.environ.get('DATABASE_STAGING_USER')
        os.environ['DATABASE_PASSWORD'] = os.environ.get('DATABASE_STAGING_PASSWORD')

    def tearDown(self):
        os.environ['TESTING'] = 'False'

    def test_get_actors_success(self):
        response = self.client().get('/api/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_actors_error(self):
        response = self.client().get('/api/actors?page=1000')
        self.assertEqual(response.status_code, 404)

    def test_get_movies_success(self):
        response = self.client().get('/api/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movies_error(self):
        response = self.client().get('/api/movies?page=1000')
        self.assertEqual(response.status_code, 404)

    def test_get_actor_success(self):
        response = self.client().get('/api/actors/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_actor_error(self):
        response = self.client().get('/api/actors/9999')
        self.assertEqual(response.status_code, 404)

    def test_get_movie_success(self):
        response = self.client().get('/api/movies/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movie_error(self):
        response = self.client().get('/api/movies/9999')
        self.assertEqual(response.status_code, 404)

    def test_delete_actor_success(self):
        response = self.client().delete('/api/actors/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor_error(self):
        response = self.client().delete('/api/actors/9999')
        self.assertEqual(response.status_code, 404)

    def test_delete_movie_success(self):
        response = self.client().delete('/api/movies/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movie_error(self):
        response = self.client().delete('/api/movies/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_actor_success(self):
        response = self.client().post('/api/actors', json={'name': 'Test Actor', 'bio': 'Test bio'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_movie_success(self):
        response = self.client().post('/api/movies', json={'title': 'Test Movie', 'release_date': '2023-01-01'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor_success(self):
        response = self.client().patch('/api/actors/1', json={'name': 'Updated Actor', 'bio': 'Updated bio'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor_error(self):
        response = self.client().patch('/api/actors/9999', json={'name': 'Updated Actor', 'bio': 'Updated bio'})
        self.assertEqual(response.status_code, 404)

    def test_update_movie_success(self):
        response = self.client().patch('/api/movies/1', json={'title': 'Updated Movie', 'release_date': '2023-01-01'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movie_error(self):
        response = self.client().patch('/api/movies/9999', json={'title': 'Updated Movie', 'release_date': '2023-01-01'})
        self.assertEqual(response.status_code, 404)

    def test_update_movie_add_actors_success(self):
        response = self.client().patch('/api/movies/1', json={'actors': [1, 2, 3]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movie_add_actors_error(self):
        response = self.client().patch('/api/movies/9999', json={'actors': [1, 2, 3]})
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
