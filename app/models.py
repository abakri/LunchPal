from flask_sqlalchemy import SQLAlchemy
from app import db, ma
import bcrypt

import hashlib, uuid

# ----------------------------
#		DATABASE MODELS
# ----------------------------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

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
    def validate_password(self, password):
        # validate the password here
        pass

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True)

    def __init__(self, jti):
        self.jti = jti
    
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
