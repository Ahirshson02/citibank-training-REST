from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from extensions import init_db

from repositories.user_repository import UserRepository
from repositories.account_repository import AccountRepository

from services.user_service import UserService
from services.account_service import AccountService

from controllers.user_controller import build_user_blueprint
from controllers.account_controller import build_account_blueprint


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    CORS(app=app, methods=["GET","POST","DELETE","PATCH"], allow_headers=["Content-Type", "Authorization"])
    from config import Config
    app.config.from_object(Config)
    init_db(app)


    @app.route("/")
    def index():
        return {"status": "ok", "service": "bank-api"}, 200

    user_repository = UserRepository()
    account_repository = AccountRepository()

    #user_service = UserService(user_repository)
    account_service = AccountService(account_repository, user_repository)

    #app.register_blueprint(build_user_blueprint(user_service))
    app.register_blueprint(build_account_blueprint(account_service))

    # with app.app_context():
    #     db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, use_reloader=False)
