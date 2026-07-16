from mongoengine import connect
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def init_db(app):
    connect(
        host=app.config["MONGODB_SETTINGS"]["host"]
    )