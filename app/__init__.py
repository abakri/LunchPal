from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ----------------------------
#		APP CONFIG
# ----------------------------

class Config(object):
    SECRET_KEY = "S3CR3TK3Y"
    SQLALCHEMY_DATABASE_URI = "postgres://lunchpal:lunchpal@localhost:5432/lunchpaldb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_ENABLE_EMAIL = True
    USER_EMAIL_SENDER_EMAIL = "lunchpal@suckmy.ass"

# ----------------------------
#		FLASK EXTENSIONS
# ----------------------------

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
migrate = Migrate(app, db)

# ----------------------------
#		RESOURCE URLS
# ----------------------------
from app import resources

api.add_resource(resources.UserResource, "/User", "/User/<string:username>")

# ----------------------------
#		START APP
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)