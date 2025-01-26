from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from api.models import Order, User, Product, OrderProduct
from api.schemas import ProductSchema
from api.schemas.orders import OrderSchema
from app import db

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        order_schema = OrderSchema()
        order_data = order_schema.load(request.json)

        user = User.query.get(order_data.user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        new_order = Order(
            user_id=order_data.user_id,
        )

        db.session.add(new_order)
        db.session.commit()

        return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201
    except Exception as e:
        print(f"Error creating an order: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@orders_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@orders_bp.route('/orders/<int:order_id>/products', methods=['GET'])
def get_products_in_order(order_id):
    try:
        order = Order.query.get(order_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        products = db.session.query(Product).join(OrderProduct).filter(OrderProduct.order_id == order_id).all()
        products_schema = ProductSchema(many=True)
        products_json = products_schema.dump(products)

        return jsonify(products_json), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@orders_bp.route('/orders/<int:order_id>/products', methods=['POST'])
def add_product_to_order(order_id):
    try:
        order_data = request.get_json()
        product_id = order_data.get("product_id")

        order = Order.query.get(order_id)
        product = Product.query.get(product_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404
        if not product:
            return jsonify({"error": "Product not found"}), 404

        existing_entry = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
        if existing_entry:
            return jsonify({"error": "Product already in the order"}), 400

        order_product = OrderProduct(order_id=order_id, product_id=product_id)

        db.session.add(order_product)
        db.session.commit()

        return jsonify({"message": "Product added to order"}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@orders_bp.route('/orders/<int:order_id>/products/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id: int, product_id: int):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        order_product = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
        if not order_product:
            return jsonify({"error": "Product not in order"}), 400

        db.session.delete(order_product)
        db.session.commit()

        return jsonify({"message": "Product removed from order"}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@orders_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        orders = Order.query.filter_by(user_id=user_id).all()
        orders_schema = OrderSchema(many=True)
        orders_json = orders_schema.dump(orders)

        return jsonify(orders_json), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
