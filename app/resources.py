from flask import jsonify, request
from flask_restful import Api, Resource, reqparse
from app import api, db
from app.models import User, UserSchema, RevokedToken, RevokedTokenSchema
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()

# ----------------------------
#		SCHEMA VARIABLES
# ----------------------------

user_schema = UserSchema()
users_schema = UserSchema(many=True)

revokedtoken_scheme = RevokedTokenSchema()

class UserRegistration(Resource):
    def post(self): # register user
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()

        # check if the user already exists
        if User.query.filter_by(username=data['username']).first():
            return {'message' : f"user with username {data['username']} already exists"}

        user = User(
            data['username'],
            data['password']
        )

        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message' : f"user {user_schema.dump(user)} was successfully created",
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }
        except:
            return {'message' : 'Something went wrong!'}, 500


class UserLogin(Resource):
    def post(self):
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()
        
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message' : f"user {data['username']} doesn't exists"}, 400
        
        if user.check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message' : f"Logged in as {data['username']}",
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }
        else:
            return {'message' : f"Wrong password"}, 400
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti)
            db.session.add(revoked_token)
            db.session.commit()
            return {'message': 'Access has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jti()['jti']
        try:
            revoked_token = RevokedToken(jti)
            revoked_token.add()
            return {'message': 'Access has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500      


# this is used when we want to give the user a new access token without asking them to refresh
# so essentially whenever they want to access protected api, if they don't have an access token, then
# they should attempt to refresh token first
# *** perhaps find a way to auto-refresh tokens in react ***
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    def get(self):
        return users_schema.dump(User.query.all())

      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }


class UserResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user_schema.jsonify(user)
        else:
            return f"User {username} not found", 400