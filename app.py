from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS

# -----------------------------------
# Initialize the Flask application
# -----------------------------------
app = Flask(__name__)
CORS(app)

# Apply the configurations to the app
app.config.from_object(Config)

# Initialize SQLAlchemy, Marshmallow and JWT for the app
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)

from api.routes import api_routes_bp

app.register_blueprint(api_routes_bp, url_prefix='/api')

# Ensure all tables defined in models are created in the database
with app.app_context():
    db.create_all()
    print("Tables created successfully!")

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
