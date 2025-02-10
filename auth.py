from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import users_collection  # Create a users collection in MongoDB

auth_bp = Blueprint('auth', __name__)

# ------------------------ USER LOGIN & JWT GENERATION ------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Find user in the database
    user = users_collection.find_one({"username": username})

    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200

# ------------------------ PROTECTED ROUTE (TEST) ------------------------

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}! You have access to this route."}), 200
