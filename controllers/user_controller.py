
from flask import Blueprint, request, jsonify
from services.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token

user_bp = Blueprint("user", __name__, url_prefix="/api/users")


def build_user_blueprint(user_service: UserService) -> Blueprint:

    @user_bp.route("/test", methods=["GET"])
    def test():
        print("in test")
        return {"data": "test working"}, 200

    @user_bp.route("/register", methods=["POST"])
    def register():
        print("IN REGISTER")
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        username = data.get("username")
        role = data.get("role", "user")

        try:
            user = user_service.register(email, username, role)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        return jsonify({"user": user.to_dict()}), 201

    @user_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        username = data.get("username")

        user, access_token, refresh_token = user_service.login(email, username)

        return {"data": {"user": user.to_dict(), "access_token": access_token, "refresh_token": refresh_token}}, 200

    return user_bp
