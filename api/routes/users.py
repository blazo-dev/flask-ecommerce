from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.models import User
from api.schemas import UserSchema
from app import db

users_bp = Blueprint('users', __name__)


# Example route: Get all users
@users_bp.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve all users.
    ---
    Responses:
      200:
        description: A list of users in JSON format.
      500:
        description: Internal server error.
    """
    try:
        # Query all users from the database
        users = User.query.all()

        # Serialize users using the schema
        users_schema = UserSchema(many=True)
        users_json = users_schema.dump(users)

        # Return the serialized data as JSON
        return jsonify(users_json), 200
    except Exception as e:
        # Log the error (optional) and return an error response
        print(f"Error retrieving users: {e}")
        return jsonify({"error": "An error occurred while fetching users."}), 500


# Example route: Create a new user
@users_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    ---
    Request Body (JSON):
      {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepassword",
        "address": "123 Main Street"
      }
    Responses:
      201:
        description: User successfully created.
      400:
        description: Validation error or missing data.
      500:
        description: Internal server error.
    """
    try:

        user_schema = UserSchema()
        user_data: User = user_schema.load(request.json)

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            address=user_data.address
        )

        db.session.add(new_user)
        db.session.commit()

        created_user = user_schema.dump(new_user)

        return jsonify({
            "message": "User created successfully",
            "data": created_user
        }), 201

    except ValidationError as e:
        return jsonify({
            "error": "Validation error",
            "messages": e.messages
        }), 400

    except IntegrityError as e:
        db.session.rollback()

        if "Duplicate entry" in str(e.orig) and "users.email" in str(e.orig):
            return jsonify({"error": "This email is already in use. Please use a different one."}), 409

        return jsonify({"error": "Database integrity error", "message": str(e)}), 500

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while creating the user."
        }), 500
