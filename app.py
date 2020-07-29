import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import datetime

from models import db, setup_db, Movie, Actor


def to_date(date):
    #print(date)
    # Date parsed as DD/MM/YYYY or DD-MM-YYYY
    if "/" in date:
        parts = date.split('/')
    elif "-" in date:
        parts = date.split('-')
    if not (len(parts) == 3):
        abort(400)
    #print("DATE:", parts[1], type(int(parts[1])))
    return datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        return "Welcome to the Casting Agency App"

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.name).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify(
            {
                'success': True,
                'actors': formatted_actors
            }
        )

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.title).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify(
            {
                'success': True,
                'actors': formatted_movies
            }
        )

    @app.route('/actors', methods=['POST'])
    def add_actor():
        try:
            body = request.get_json()
            if not ('name' in body and 'age' in body and 'gender' in body):
                abort(400)
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')
            actor = Actor(name, age, gender)
            actor.insert()
            return jsonify(
                {
                    'success': True,
                    'created': actor.id
                }
            )
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies', methods=['POST'])
    def add_movie():
        try:
            body = request.get_json()
            if not ('title' in body and 'release_date' in body):
                abort(400)
            title = body.get('title')
            release_date = body.get('release_date')

            movie = Movie(title, to_date(release_date))
            movie.insert()
            return jsonify(
                {
                    'success': True,
                    'created': movie.id
                }
            )
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor.id
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie.id
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        try:
            body = request.get_json()
            if not ('name' in body and 'age' in body and 'gender' in body):
                abort(400)
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')
            actor = Actor.query.get(actor_id)
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender
            actor.update()
            return jsonify({
                'success': True,
                'updated': actor.id
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        try:
            body = request.get_json()

            if (body is None) or ('title' not in body and 'release_date' not in body):
                #print("Aborted")
                abort(400)

            title = body.get('title')
            #print(title)
            release_date = body.get('release_date')
            movie = Movie.query.get(movie_id)
            if title is not None:
                movie.title = title
                #print(title)
            if release_date is not None:
                movie.release_date = to_date(release_date)
                #print(release_date)

            movie.update()
            return jsonify({
                'success': True,
                'updated': movie.id
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    return app


app = create_app()

if __name__ == '__main__':
    app.run()