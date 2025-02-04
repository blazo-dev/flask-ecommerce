from flask import Blueprint

from .auth import auth_bp
from .users import users_bp
from .products import products_bp
from .orders import orders_bp

# Create a Blueprint to group-all routes
api_routes_bp = Blueprint('api_routes', __name__)

# Register individual Blueprints
api_routes_bp.register_blueprint(users_bp)
api_routes_bp.register_blueprint(products_bp)
api_routes_bp.register_blueprint(orders_bp)
api_routes_bp.register_blueprint(auth_bp)
