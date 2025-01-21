from flask import Blueprint, jsonify

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify({"message": "List of orders... :D"})


@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create an order"""
    return jsonify({"message": "List of orders... :D"})
