from flask import Blueprint, request, jsonify
from app.controllers.users_controller import (
    get_users_controller,
    login_controller
)

users_bp = Blueprint("users", __name__)


@users_bp.get("/api/users")
def get_users_route():
    username = request.args.get("username")
    mobile = request.args.get("mobile")

    result = get_users_controller(username, mobile)
    return jsonify(result)


@users_bp.post("/api/login")
def login_route():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")
    token = data.get("token")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    result = login_controller(username, password, token)
    if not result:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "status": "success",
        **result
    })
