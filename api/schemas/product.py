from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.models import Product
from app import ma


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
