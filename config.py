import os
class Config:
    MONGODB_SETTINGS = {
        "host": (
            os.environ["MONGODB_URI"]
        )
    }
    DEBUG = True
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expires in 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # Refresh token expires in 1 day
