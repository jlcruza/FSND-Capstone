import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from database.models import setup_db
from auth.auth import AuthError, requires_auth


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "moviecenter"
        self.database_path = "postgres://{}@{}/{}".format(
            'jorgecruz', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.casting_assistance = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpYczduNnp3NmNFNHRwSUhfTDdRVCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJkNjY5OTYyZDAzYzBjNmZlMjIzYjciLCJhdWQiOiJleGVjdXRpdmUiLCJpYXQiOjE1ODk3NTU3MTgsImV4cCI6MTU4OTg0MjExOCwiYXpwIjoibzhqMGYzREVOOXYzVVJ4QVhuMW82NXZKb3J4Wk5MSjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.OJw6yxxP66XU9J30UMkh4nizM7CjZS91A3V1yh83pjN9MZk7p0NCSYXP7PgK4krSUP5afx0NUBtwrVet7TEGCShaYkbY9GFyW9Suwlvpg-qMlB4ShbeSGiA0cG40mKxw6CDn6QZRRlMAncF3YlmbVwc9Uh_7XxLv1aCS2_GEP_eJreawanPaRE8tYEflDNwxR8mkWgTyZoA1PzvI-c8cG-tEdVN9y87byYqN2jwRYiFrTC8r2l92YgUZ2pZZIpeD0irBgqO7KneEogFq3FBmDdwgL35DcJTLngJPg1xh1vwGPUwTH-qAoVGricMFz_KYu81SSS74x43L_wefQZM3NA'}
        self.casting_director = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpYczduNnp3NmNFNHRwSUhfTDdRVCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJkNjZjOTA1NWE0YjBjNmZjZmM4NzUiLCJhdWQiOiJleGVjdXRpdmUiLCJpYXQiOjE1ODk3NTU3MzcsImV4cCI6MTU4OTg0MjEzNywiYXpwIjoibzhqMGYzREVOOXYzVVJ4QVhuMW82NXZKb3J4Wk5MSjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.Bvp9eheBCVukYBUFa0LOXL3xu1c6bGFsHV_8DHJCCv2s6LDT1g_1F6-6zqtMzAC84bDFy8h6LgotfIWYMkUYF7VpbF96t8ab-h6uwtodWI34dE2zEfRDsvgmitsCn8GFC3cWH3wU-aRg34H0JZHRH-euY2TqBZUpfyGJIIzlyVLpamZl59NOe4rSW_MB60iyMFjASDZyA902IxStDsVZNTLhXFEgFlcRU3eAu2JdVmiB3kuRq-Qsx89XYsEwEvy0aaatwDYgGgY-ddeiSnL2m19L6AGsbXxos9GHxnUHjlqgimcy2xDP_EiAezo1-FP4IhFfuM5x5q1i6_JMVKdwhw'}
        self.executive_producer = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpYczduNnp3NmNFNHRwSUhfTDdRVCJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJkNjY2OGNiODAwOTBjN2NjMzM2NjciLCJhdWQiOiJleGVjdXRpdmUiLCJpYXQiOjE1ODk3NTU3MDQsImV4cCI6MTU4OTg0MjEwNCwiYXpwIjoibzhqMGYzREVOOXYzVVJ4QVhuMW82NXZKb3J4Wk5MSjEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.cFG1nd_tFbVbcVDLI9jRkwKoCtZqm31jT_2be4e_WBDJfHPBXGXswB4ohXOca9gMqjAbx235Dh0qIXbUfzWfni9JfBu9e2odR3vgBvz4T78z84YRgBPew92of5iIf8n_QpAnwVvealbBvcQ_wNzJozrle4gpGRBuWZNej6XKCA6Kul4eDFJR-JV8WtsHxI2_HOe1xfasIxSi-t-aH2y1L3A_v6p3A0CjmJ-_5qYevJlsrkpsJzEdQpZfxP5Z4iJASzJIf3fB38DUZLH1m3cJqXmFlmsiWwU8Ub6nz9IrwVlrPo7k-AkirBxmkBPG3ZAoez8slsbWakutsM-t4J3vjw'}

        self.new_actor = {
            'name': 'Test Actor',
            'age': 1,
            'gender': 'Other',
            'picture_link': 'test.com',
            'bio': 'Actor that only perform tests.'
        }

        self.updated_actor = {
            'name': 'Test Actor v2',
            'age': 2,
            'gender': 'Other',
            'picture_link': 'test2.com',
            'bio': 'Actor that perform tests instead of movies.'
        }

        self.new_movie = {
            'title': 'Test Movie',
            'released': '2020-05-20',
            'picture_link': 'test.com',
            'synopsis': 'It is only a horror movie if the test fail.'
        }

        self.updated_movie = {
            'title': 'Test Movie v2',
            'released': '2020-05-21',
            'picture_link': 'test2.com',
            'synopsis': 'Otherwise, it is my favorite movie.'
        }

        self.casting1 = {
            'actors_id': 1,
            'movies_id': 2
        }

        self.casting2 = {
            'actors_id': 2,
            'movies_id': 2
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_casting_assistance(self):
        response = self.client().get('/actors', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total'])

    def test_get_actors_casting_director(self):
        response = self.client().get('/actors', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total'])

    def test_get_actors_executive_producer(self):
        response = self.client().get('/actors', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total'])

    def test_401_get_actors_public(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_get_movies_casting_assistance(self):
        response = self.client().get('/movies', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['total'])

    def test_get_movies_casting_director(self):
        response = self.client().get('/movies', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['total'])

    def test_get_movies_executive_producer(self):
        response = self.client().get('/movies', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['total'])

    def test_401_get_movies_public(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_create_actors_casting_assistance(self):
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_create_actors_casting_director(self):
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_actors_executive_producer(self):
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_create_actors_public(self):
        response = self.client().post('/actors', json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_create_movies_casting_assistance(self):
        response = self.client().post('/movies', json=self.new_movie,
                                      headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_403_create_movies_casting_director(self):
        response = self.client().post('/movies', json=self.new_movie,
                                      headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_create_movies_executive_producer(self):
        response = self.client().post('/movies', json=self.new_movie,
                                      headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_create_movies_public(self):
        response = self.client().post('/movies', json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_update_actors_casting_assistance(self):
        response = self.client().patch('/actors/1', json=self.updated_actor,
                                       headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_update_actors_casting_director(self):
        response = self.client().patch('/actors/1', json=self.updated_actor,
                                       headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actor'])

    def test_update_actors_executive_producer(self):
        response = self.client().patch('/actors/2', json=self.updated_actor,
                                       headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actor'])

    def test_401_update_actors_public(self):
        response = self.client().patch('/actors/1', json=self.updated_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_update_movies_casting_assistance(self):
        response = self.client().patch('/movies/1', json=self.updated_movie,
                                       headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_update_movies_casting_director(self):
        response = self.client().patch('/movies/1', json=self.updated_movie,
                                       headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movie'])

    def test_update_movies_executive_producer(self):
        response = self.client().patch('/movies/2', json=self.updated_movie,
                                       headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movie'])

    def test_401_update_movies_public(self):
        response = self.client().patch('/movies/1', json=self.updated_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_create_cast_casting_assistance(self):
        response = self.client().post('/cast', json=self.casting1,
                                      headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_create_cast_casting_director(self):
        response = self.client().post('/cast', json=self.casting1,
                                      headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_cast_executive_producer(self):
        response = self.client().post('/cast', json=self.casting2,
                                      headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_401_create_cast_public(self):
        response = self.client().post('/cast', json=self.casting2)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_get_actors_cast_casting_assistance(self):
        response = self.client().get('/actors/1/cast', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_actors_cast_casting_director(self):
        response = self.client().get('/actors/1/cast', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_actors_cast_executive_producer(self):
        response = self.client().get('/actors/1/cast', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_401_get_actors_cast_executive_producer(self):
        response = self.client().get('/actors/1/cast')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_get_movie_cast_casting_assistance(self):
        response = self.client().get('/movies/1/cast', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movie_cast_casting_director(self):
        response = self.client().get('/movies/1/cast', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movie_cast_executive_producer(self):
        response = self.client().get('/movies/1/cast', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_get_movie_cast_public(self):
        response = self.client().get('/movies/1/cast')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_get_movie_cast_casting_assistance(self):
        response = self.client().get('/movies/1/nocast', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movie_cast_casting_director(self):
        response = self.client().get('/movies/1/nocast', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movie_cast_executive_producer(self):
        response = self.client().get('/movies/1/nocast', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_get_movie_cast_public(self):
        response = self.client().get('/movies/1/nocast')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_delete_casting_casting_assistance(self):
        response = self.client().delete('/cast/1/1', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_delete_casting_casting_director(self):
        response = self.client().delete('/cast/' +
                                        str(self.casting1['movies_id'])+'/'+str(self.casting1['actors_id']), headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_casting_executive_producer(self):
        response = self.client().delete('/cast/' +
                                        str(self.casting2['movies_id'])+'/'+str(self.casting2['actors_id']), headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_401_delete_casting_public(self):
        response = self.client().delete('/cast/1/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_delete_actor_casting_assistance(self):
        response = self.client().delete('/actors/1', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_delete_actor_casting_director(self):
        response = self.client().delete('/actors/3', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_actor_executive_producer(self):
        response = self.client().delete('/actors/4', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_401_delete_actor_public(self):
        response = self.client().delete('/actors/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_403_delete_movies_casting_assistance(self):
        response = self.client().delete('/movies/1', headers=self.casting_assistance)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_403_delete_movies_casting_director(self):
        response = self.client().delete('/movies/1', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "action not allowed for this user")

    def test_delete_movies_executive_producer(self):
        response = self.client().delete('/movies/3', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_401_delete_actor_public(self):
        response = self.client().delete('/movies/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
