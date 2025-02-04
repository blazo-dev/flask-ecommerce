from app import db


class OrderProduct(db.Model):
    __tablename__ = 'order_product'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)

    # Prevent duplicate entries for the same product in the same order
    __table_args__ = (db.UniqueConstraint('order_id', 'product_id', name='unique_order_product'),)
