from flask import session
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from app import db, ma
from enum import Enum
import hashlib, uuid, bcrypt

# ----------------------------
#		DATABASE MODELS
# ----------------------------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # related data
    userprofile = db.relationship('UserProfile', backref='user', lazy=True, uselist=False) # uselist = False for one to one
    # signals = db.relationship('Signal', backref='user', lazy=True)

    # User Authentication fields
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username

        # hash the password
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt(14))
        self.password_hash = password_hash
    
    def check_password(self, password):
        return bcrypt.checkpw(password, self.password_hash)

    @staticmethod
    def current_user():
        return User.query.filter_by(id=session['user_id']).first()


class UserProfile(db.Model):
    __tablename__ = 'userprofiles'
    id = db.Column(db.Integer, primary_key=True)

    # related data
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    userinterests = db.relationship('UserInterest', backref='userprofile', lazy=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.String(20), nullable=False) # maybe make unique?
    age = db.Column(db.Integer, nullable=False)
    occupation = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True) 


# class Signal(db.Model):
#     __tablename__ = 'signals'
#     id = db.Column(db.Integer, primary_key=True)

#     # related data
#     institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     active = db.Column(db.Boolean, nullable=False)
#     time = db.Column(db.DateTime, nullable=False, unique=True)
#     place = db.Column(db.String(20), nullable=False)


class Institution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)

    # related data
    members = db.relationship('UserProfile', backref='institution')
    # signals = db.relationship('UserSignal', backref='institution')

    name = db.Column(db.String(50), nullable=False, unique=True)


class Interest(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)

    # related data
    userinterests = db.relationship('UserInterest', backref='interest')

    name = db.Column(db.String(50), nullable=False, unique=True)


class UserInterest(db.Model):
    __tablename__ = 'user_interests'
    id = db.Column(db.Integer, primary_key=True)

    # related data
    userprofile_id = db.Column(db.Integer, db.ForeignKey('userprofiles.id'))
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'))


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True)
    
    @classmethod
    def is_blacklisted(cls, jti):
        if cls.query.filter_by(jti=jti).first():
            return True
        return False

# ----------------------------
#	    OBJECT SCHEMAS
# ----------------------------

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class RevokedTokenSchema(ma.ModelSchema):
    class Meta:
        model = RevokedToken


class UserProfileSchema(ma.ModelSchema):
    class Meta:
        model = UserProfile


class InstitutionSchema(ma.ModelSchema):
    class Meta:
        model = Institution


class InterestSchema(ma.ModelSchema):
    class Meta:
        model = Interest


class UserInterestSchema(ma.ModelSchema):
    class Meta:
        model = UserInterest

# class SignalSchema(ma.ModelSchema):
#     class Meta:
#         model = UserInterest