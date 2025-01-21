from flask import Blueprint, jsonify

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get all products.
    """
    return jsonify({"message": "List of products"})


# Example route: Add a product
@products_bp.route('/products', methods=['POST'])
def add_product():
    """
    Add a new product.
    """
    # Replace it with logic to add product
    return jsonify({"message": "Product added"})
