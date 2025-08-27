from flask import Blueprint, request, jsonify
from models import db, User

user_bp = Blueprint("user_bp", __name__)

# Add user
@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password_hash = data.get("password")
    if not username or not email or not password_hash:
        return {"error": "username, email, and password are required"}, 400

    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return {"message": f"User {username} added!"}, 201

# Get all users
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role
    } for u in users])

# Get single user
@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }
