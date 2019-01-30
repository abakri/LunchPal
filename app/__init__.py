from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ----------------------------
#		APP CONFIG
# ----------------------------

class Config(object):
    SECRET_KEY = "S3CR3TK3Y"
    SQLALCHEMY_DATABASE_URI = "postgres://chow@localhost:5432/chowdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# ----------------------------
#		FLASK EXTENSIONS
# ----------------------------

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)
migrate = Migrate(app, db)

# ----------------------------
#		MIDDLEWARE
# ----------------------------

# from app import models

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedToken.is_blacklisted(jti)

# ----------------------------
#		RESOURCE URLS
# ----------------------------
from app import resources

api.add_resource(resources.UserResource, "/User", "/User/<string:username>")
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

# ----------------------------
#		START APP
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)