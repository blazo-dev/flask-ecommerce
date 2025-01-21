from flask import Blueprint, jsonify, request

users_bp = Blueprint('users', __name__)


# Example route: Get all users
@users_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users.
    """
    # Replace it with database logic
    return jsonify({"message": "List of users"})


# Example route: Create a new user
@users_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    """
    data = request.json
    # Replace it with logic to save user to the database
    return jsonify({"message": "User created", "data": data})
