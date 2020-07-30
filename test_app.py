import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, to_date
from models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "casting_agency_test"
        # self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'Postgres@1', 'localhost:5432',
        #                                                       self.database_name)
        database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_delete_actor(self):
        actor = Actor(name='Test Actor', age=20, gender="Male")
        actor.insert()
        actor_id = actor.id

        actors_before = Actor.query.all()

        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)
        actors_after = Actor.query.all()
        actor = Actor.query.filter(Actor.id == actor.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertTrue(len(actors_before) - len(actors_after) == 1)

    def test_delete_movie(self):
        movie = Movie(title='Test Movie', release_date=to_date("12/2/2012"))
        movie.insert()
        movie_id = movie.id

        movies_before = Movie.query.all()

        res = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(res.data)
        movies_after = Movie.query.all()
        movie = Movie.query.filter(Movie.id == movie.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertTrue(len(movies_before) - len(movies_after) == 1)

    def test_failing_delete_actor(self):
        res = self.client().delete('/actors/99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_failing_delete_movie(self):
        res = self.client().delete('/movies/99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_add_actor(self):
        actor = {
            'name': 'Test Actor',
            'age': 20,
            'gender': 'Female'
        }
        actors_before = len(Actor.query.all())
        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)
        actors_after = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(actors_after, actors_before + 1)

    def test_add_movie(self):
        movie = {
            'title': 'Test Movie',
            'release_date': "12/2/2012"
        }
        movies_before = len(Movie.query.all())
        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)
        movies_after = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(movies_after, movies_before + 1)

    def test_failing_add_actor(self):
        actor = {
            'name': 'Test Actor',
            'gender': 'Female'
        }
        actors_before = Actor.query.all()
        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)
        actors_after = Actor.query.all()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        self.assertTrue(len(actors_before) == len(actors_after))

    def test_failing_add_movie(self):
        movie = {
            'title': 'Test Movie',
            'release_date': to_date("12/2/2012")
        }
        movies_before = len(Movie.query.all())
        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)
        movies_after = len(Movie.query.all())

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        self.assertTrue(movies_before == movies_after)

    def test_patch_actors(self):
        actor = {
            'name': 'New Actor',
            'age': 20,
            'gender': 'Female'
        }
        res = self.client().post('/actors', json=actor)
        data = json.loads(res.data)
        actor_id = data['created']
        updated_actor = {'name': 'New Actor'}
        res = self.client().patch(f'/actors/{actor_id}', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], actor_id)

    def test_patch_movies(self):
        movie = {
            'title': 'New Movie',
            'release_date': "12/2/2012"
        }
        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)
        movie_id = data['created']
        updated_movie = {'title': 'New Movie'}
        res = self.client().patch(f'/movies/{movie_id}', json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], movie_id)

    def test_failing_patch_actors(self):
        updated_actor = {'name': 'New Actor'}
        res = self.client().patch(f'/actors/99999', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_failing_patch_movies(self):
        updated_movie = {'title': 'New Movie'}
        res = self.client().patch(f'/movies/99999', json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
