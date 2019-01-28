from flask import jsonify, request
from flask_restful import Api, Resource, reqparse
from app import api, db
from app.models import User, UserSchema

parser = reqparse.RequestParser()

# ----------------------------
#		SCHEMA VARIABLES
# ----------------------------

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user_schema.jsonify(user)
        else:
            return f"User {username} not found", 400

    def post(self):
        data = request.get_json()
        new_user = User(data['username'], data['password'])
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user) 