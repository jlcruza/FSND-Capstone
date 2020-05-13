import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE')
        return response


    ''' 4xx - Client Error Handlers '''
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

    ''' 5xx - Internal Server Error Handler '''
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Error: Internal Server Error ocurred"
        }), 500

    return app