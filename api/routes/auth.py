from flask import Blueprint
from flask_jwt_extended import create_access_token

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
