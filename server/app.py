#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

@app.before_request
def check_if_logged_in():
    open_access_list = [
        'signup',
        'login',
        'check_session'
    ]

    if (request.endpoint) not in open_access_list and (not session.get('user_id')):
        return {'error': '401 Unauthorized'}, 401


class Signup(Resource):
    def post(self):
        # breakpoint()
        # Be handled in a Signup resource with a post() method.
        request_json= request.get_json()

        # Save a new user to the database with their username, encrypted password, image URL, and bio.
        username = request_json.get('username')
        password = request_json.get('password')
        image_url = request_json.get('image_url')
        bio = request_json.get('bio')

        user = User(
            username=username,
            image_url = image_url,
            bio=bio)

        user.password_hash = password

        # Save the user's ID in the session object as user_id.
        # breakpoint()
        try:
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            # Return a JSON response with the user's ID, username, image URL, and bio; and an HTTP status code of 201 (Created).
            return user.to_dict(), 201
        # Return a JSON response with the error message, and an HTTP status code of 422 (Unprocessable Entity).
        except IntegrityError:
            return {'error': '422 Unprocessable Entity'}, 422
        
    
class CheckSession(Resource):
    # Be handled in a CheckSession resource with a get() method.
    def get(self):
        user_id = session['user_id']
        # (if their user_id is in the session object): Return a JSON response with the user's ID, username, image URL, and bio; and an HTTP status code of 200 (Success).
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            # import ipdb
            # ipdb.set_trace()
            # breakpoint()

            return user.to_dict(), 200
        # if not in session: Return a JSON response with an error message, and a status of 401 (Unauthorized).
        return {}, 401


class Login(Resource):
# incorporate bcrypt to create a secure password. Attempts to access the password_hash should be met with an AttributeError.

    def post(self):
        username = request.get_json()['username']
        user = User.query.filter(user.username == username)

        password = request.get_json()['password']

        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid username or password'}, 401
    

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204

class RecipeIndex(Resource):
    def get(self):
        user = User.query.filter(User.id == session['user_id']).first()
        return [recipe.to_dict() for recipe in user.recipes], 200
    
    def post(self):
        request_json = request_json()
        
        title = request_json['title']
        instructions = request_json['instructions']
        minutes_to_complete = request_json['minutes_to_complete']

        try:
            recipe = Recipe(
                title=title,
                instructions = instructions,
                minutes_to_complete = minutes_to_complete,
                user_id = session['user_id'],
            )

            db.session.add(recipe)
            db.session.commit()

            return recipe.to_dict(), 201
        
        except IntegrityError:
            return {'error': '422 Unprocessable Entity'}, 422




api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)