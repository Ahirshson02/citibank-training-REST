from mongoengine import connect


def init_db(app):
    connect(
        host=app.config["MONGODB_SETTINGS"]["host"]
    )