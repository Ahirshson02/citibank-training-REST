
from flask import Blueprint, request, jsonify
from services.user_service import UserService
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

        try:
            user = user_service.register(email, username)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        return jsonify(user.to_dict()), 201

    @user_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        username = data.get("username")

        user = user_service.login(email, username)

        return jsonify({"user_id": user.to_dict()}), 200

    return user_bp
