import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH')
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def get_actors(jwt):
        '''
        Retrieves all actors from the database.
        Requieres [read:actors] permission.
        '''

        try:
            actors_query = Actor.query.all()

            data = []
            for actor in actors_query:
                data.append(actor.format())

            return jsonify({
                'success':True,
                'actors':data,
                'total':len(data)
            })
        
        except:
            abort(422)


    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies(jwt):
        '''
        Retrieves all movies from the database.
        Requieres [read:movies] permission.
        '''

        try:
            movies_query = Movie.query.all()

            data = []
            for movie in movies_query:
                data.append(movie.format())

            return jsonify({
                'success':True,
                'actors':data,
                'total':len(data)
            })
        
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, id):
        '''
        Permantly delete an actor from the database.
        Requieres [delete:actors] permission.
        '''

        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)
            
            actor.delete()
            
            return jsonify({
                'success':True,
                'delete':id
            })
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, id):
        '''
        Permantly delete a movie from the database.
        Requieres [delete:movies] permission.
        '''

        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort(404)
            
            movie.delete()
            
            return jsonify({
                'success':True,
                'delete':id
            })
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actors(jwt):
        '''
        Creates an actor in the database.
        Requieres [create:actors] permission.
        '''
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        picture_link = body.get('picture_link', None)

        if name is None:
            abort(400)
        elif age is None:
            abort(400)
        elif gender is None:
            abort(400)

        try:
            actor = Actor(
                name=name,
                age=age,
                gender=gender,
                picture_link=picture_link
                )

            actor.insert()
            
            return jsonify({
                'success':True,
                'created':actor.id
            })
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movies(jwt):
        '''
        Creates a movie in the database.
        Requieres [create:movies] permission.
        '''
        body = request.get_json()
        title = body.get('title', None)
        released = body.get('released', None)
        picture_link = body.get('picture_link', None)

        if title is None:
            abort(400)
        elif released is None:
            abort(400)

        try:
            movie = Movie(
                title=title,
                released=released,
                picture_link=picture_link
                )

            movie.insert()
            
            return jsonify({
                'success':True,
                'created':movie.id
            })
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(jwt, id):
        '''
        Updates an actor's information in the database.
        Requieres [patch:actors] permission.
        '''
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        picture_link = body.get('picture_link', None)

        if name is None and age is None and gender is None and picture_link is None:
            abort(400)

        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)
            
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender
            if picture_link is not None:
                actor.picture_link = picture_link
            
            actor.update()
            
            return jsonify({
                'success':True,
                'actor':actor.format()
            })
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(jwt, id):
        '''
        Updates a movie's information in the database.
        Requieres [patch:movies] permission.
        '''
        body = request.get_json()
        title = body.get('title', None)
        released = body.get('released', None)
        picture_link = body.get('picture_link', None)

        if title is None and released is None and picture_link is None:
            abort(400)

        try:
            movie = Movie.query.filter(Actor.id == id).one_or_none()

            if movie is None:
                abort(404)
            
            if title is not None:
                movie.title = title
            if released is not None:
                movie.released = released
            if picture_link is not None:
                movie.gender = picture_link
            
            movie.update()
            
            return jsonify({
                'success':True,
                'movie':movie.format()
            })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Error: A bad request was made"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Error: The requested resource was not found"
        }), 404

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Error: Forbidden method used"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Error: Cannot proccess request"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Error: Internal Server Error ocurred"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
        }), e.status_code
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)