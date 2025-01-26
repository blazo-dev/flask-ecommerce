from datetime import datetime, timezone

from app import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    products = db.relationship('Product', secondary='order_product', backref='orders')
