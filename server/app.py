#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        if password and username:
            new_user = User(username=username)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):

        if session['user_id']:
            user = User.query.filter_by(id = session['user_id']).first().to_dict()
            return user, 200
        
        return {}, 204

class Login(Resource):
    
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter_by(username = username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Login, '/login', endpoint='login')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
