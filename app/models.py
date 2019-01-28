from flask_sqlalchemy import SQLAlchemy
from app import db, ma

# ----------------------------
#		DATABASE MODELS
# ----------------------------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# ----------------------------
#	    OBJECT SCHEMAS
# ----------------------------


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
