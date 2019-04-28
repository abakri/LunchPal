import time

from datetime import datetime
from flask import jsonify, request
from flask_restful import Api, Resource, reqparse
from app import api, db
from app.models import (User, UserSchema, RevokedToken, RevokedTokenSchema,
                        UserProfile, UserProfileSchema, Institution, InstitutionSchema,
                        Interest, InterestSchema, UserInterest, UserInterestSchema)
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()

# ----------------------------
#		SCHEMA VARIABLES
# ----------------------------

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_profile_schema = UserProfileSchema()
user_profiles_schema = UserProfileSchema(many=True)

institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)

interest_schema = InterestSchema()
interests_schema = InterestSchema(many=True)

userinterest_schema = UserInterestSchema()

# signal_schema = SignalSchema()
# signals_schema = SignalSchema(many=True)

revokedtoken_scheme = RevokedTokenSchema()

class UserRegistration(Resource):
    def post(self): # register user
        # we make them required for the parser so we don't have to worry about json validation
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('phone_number', required=True)
        parser.add_argument('age', required=True)
        parser.add_argument('institution_id', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('occupation', required=True) 
        data = parser.parse_args()

        # check if the user already exists
        if User.query.filter_by(username=data['username']).first():
            return {'message': f"user with username {data['username']} already exists"}, 400

        if Institution.query.filter_by(id=data['institution_id']).first():
            institution = Institution.query.filter_by(id=data['institution_id']).first()
        else:
            return {'message': f"institution with id {data['institution_id']} does not exist"}, 400

        user = User(
            data['username'],
            data['password']
        )

        user_profile = UserProfile(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            age=data['age'],
            email=data['email'],
            occupation=data['occupation']
        )

        # set the Foreign Keys
        user_profile.user = user
        user_profile.institution = institution

        try:
            db.session.add(user)
            db.session.add(user_profile)
            db.session.commit()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': f"user {user_schema.dump(user)} was successfully created",
                'user_id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        except:
            return {'message': 'Something went wrong!'}, 500


class UserLogin(Resource):
    def post(self):
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()
        
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': f"user {data['username']} doesn't exists"}, 400
        
        if user.check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': f"Logged in as {data['username']}",
                'user_id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': f"Wrong password"}, 400
            
# class UpdateInterests(Resource):
#     def post(self):
#         parser.add_argument('')

# In order to access JWT protected resources, need to use the "Authorization" head
# With value "Bearer <JWT>"

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            db.session.add(revoked_token)
            db.session.commit()
            session.pop('user_id', None)
            return {'message': 'Access has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jti()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Access has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500      

# make match API


# Signal functionality

# class PostSignal(Resource):
#     @jwt_required
#     def post(self):
#         parser.add_argument('time', required=True)
#         parser.add_argument('place', required=True)

#         time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
#         signal = Signal(
#             time=time,
#             place=data['place']
#         )

#         if not signal:
#             return {'message': 'We will send you a notification once we find you a match!'}
#         else:
#             # push notif for the first person
#             return user_schema.dump(signal.user)

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


class VerifyToken(Resource):
    @jwt_required
    def post(self):
        current

      
class AllUsers(Resource):
    def get(self):
        return users_schema.dump(User.query.all())

      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'curr_user': User.current_user().id
        }


class UserResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user_schema.jsonify(user)
        else:
            return f"User {username} not found", 400