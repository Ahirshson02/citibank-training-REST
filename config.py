import os

class Config:
    mongo_uri = os.getenv("MONGODB_URI")

    if mongo_uri is None:
        raise Exception(
            f"MONGODB_URI missing. Available vars: {list(os.environ.keys())}"
        )

    MONGODB_SETTINGS = {
        "host": mongo_uri
    }


    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400