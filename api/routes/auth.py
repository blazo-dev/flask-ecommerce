from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/token', methods=['GET'])
def get_token():
    """
    Route to generate a JWT token.
    Returns:
        - A JSON response containing the JWT token.
    """
    # Create an access token with the user's identity (in this case, a static user_id of 1)
    token = create_access_token(identity={"user_id": 1})
    return {"access_token": token}


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_jwt(user)
    return jsonify({"message": "Login successful", "token": token})


def generate_jwt(user: User):
    """
    Generate a JWT token for the given user_id.
    """

    additional_claims = {"user_email": user.email}

    access_token = create_access_token(
        identity=user.email,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=12)
    )

    return access_token
