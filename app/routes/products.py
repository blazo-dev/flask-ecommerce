from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.models import Product
from app import db
from app.schemas import ProductSchema

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_products():
    """Retrieve all products."""
    try:
        # Get all products from the database
        products = Product.query.all()

        # Serialize products
        products_schema = ProductSchema(many=True)
        products_json = products_schema.dump(products)

        # Return products as JSON
        return jsonify(products_json), 200
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return jsonify({"error": "An error occurred while fetching products."}), 500


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    """Retrieve a product by ID."""
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(ProductSchema().dump(product)), 200

    except Exception as e:
        print(f"Error retrieving product <{product_id}>: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while fetching the product."
        }), 500


@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    try:
        product_schema = ProductSchema()
        product_data = product_schema.load(request.json)

        # Create new product
        new_product = Product(
            name=product_data.name,
            price=product_data.price
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product created successfully", "data": product_schema.dump(new_product)}), 201

    except ValidationError as e:
        return jsonify({"error": "Validation error", "messages": e.messages}), 400


    except Exception as e:
        print(f"Error creating product: {e}")
        return jsonify({"error": "Internal server error"}), 500


@products_bp.route('/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id: int):
    """Update an existing product."""
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Load and validate partial data for update
        product_schema = ProductSchema(partial=True)
        update_data = product_schema.load(request.json)

        if not update_data:
            return jsonify({"error": "No data provided"}), 400

        update_fields = ['name', 'price']

        # Update product fields if provided
        for field in update_fields:
            value = getattr(update_data, field, None)
            if value:
                setattr(product, field, value)

        db.session.commit()

        return jsonify({
            "message": "Product updated successfully",
            "data": product_schema.dump(product)
        }), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "messages": e.messages}), 400

    except Exception as e:
        print(f"Error updating product: {e}")
        return jsonify({"error": "Internal server error"}), 500


@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    """Delete an existing product."""
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Delete product from the database
        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "message": "Product deleted successfully",
        }), 200

    except Exception as e:
        print(f"Error deleting product: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred while deleting the product."
        }), 500
