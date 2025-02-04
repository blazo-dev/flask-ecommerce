# Import the route files to register the routes with the Blueprint
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()


def create_app():
    # -----------------------------------
    # Initialize the Flask application
    # -----------------------------------
    app = Flask(__name__)
    CORS(app)

    # Apply the configurations to the app
    app.config.from_object(Config)

    # Initialize SQLAlchemy, Marshmallow and JWT for the app
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    from app.routes import api_routes_bp

    app.register_blueprint(api_routes_bp, url_prefix='/api')

    return app
