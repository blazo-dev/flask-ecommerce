from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from api.models import User
from api.schemas import UserSchema
from app import db

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users."""
    try:
        # Get all users from the database
        users = User.query.all()

        # Serialize users
        users_schema = UserSchema(many=True)
        users_json = users_schema.dump(users)

        # Return users as JSON
        return jsonify(users_json), 200
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return jsonify({"error": "An error occurred while fetching users."}), 500


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """Retrieve a user by ID."""
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(UserSchema().dump(user)), 200

    except Exception as e:
        print(f"Error retrieving user <{user_id}>: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while fetching the user."
        }), 500


@users_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        user_schema = UserSchema()
        user_data = user_schema.load(request.json)

        # Hash password before saving
        password_hash = generate_password_hash(user_data.password)

        # Create new user
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=password_hash,
            address=user_data.address
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "data": user_schema.dump(new_user)}), 201

    except ValidationError as e:
        return jsonify({"error": "Validation error", "messages": e.messages}), 400

    except IntegrityError as e:
        db.session.rollback()
        return jsonify(
            {"error": "Email already in use." if "Duplicate entry" in str(e.orig) else "Database error"}), 409

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    """Update an existing user."""
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Load and validate partial data for update
        user_schema = UserSchema(partial=True)
        update_data = user_schema.load(request.json)

        if not update_data:
            return jsonify({"error": "No data provided"}), 400

        update_fields = ['name', 'email', 'address']

        # Update user fields if provided
        for field in update_fields:
            value = getattr(update_data, field, None)
            if value:
                setattr(user, field, value)

        db.session.commit()

        return jsonify({
            "message": "User updated successfully",
            "data": user_schema.dump(user)
        }), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "messages": e.messages}), 400

    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete an existing user."""
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete user from the database
        db.session.delete(user)

        db.session.commit()

        return jsonify({
            "message": "User deleted successfully",
        }), 200

    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while deleting the user."
        }), 500
