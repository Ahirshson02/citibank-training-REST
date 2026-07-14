"""
controllers/user_controller.py

THE CONTROLLER LAYER
----------------------
This is the only layer that knows about Flask/HTTP. Its job is:
  1. Parse the incoming request (JSON body, query params, etc.)
  2. Call the appropriate service method
  3. Translate the result (or exception) into an HTTP response + status code

Controllers should stay "thin" - no business logic here. If you see an
`if` statement checking a business rule (like "password must match"), it's
in the wrong layer.
"""
from flask import Blueprint, request, jsonify
from services.user_service import UserService
user_bp = Blueprint("user", __name__, url_prefix="/api/users")


def build_user_blueprint(user_service: UserService) -> Blueprint:
    """
    We build the blueprint via a factory function so app.py can inject the
    already-constructed service (which itself was given a repository).
    This keeps the wiring/dependency-injection in one place: app.py.
    """

    @user_bp.route("/test", methods=["GET"])
    def test():
        print("in test")
        return {"data": "test working"}, 200

    @user_bp.route("/register", methods=["POST"])
    def register():
        print("IN REGISTER")
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = data.get("password")

        try:
            user = user_service.register(email, password)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        return jsonify(user.to_dict()), 201

    @user_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = data.get("password")

        user = user_service.login(email, password)

        return jsonify({"user_id": user.id}), 200

    return user_bp
