from marshmallow import validates, fields, ValidationError

from api.models import Product
from app import ma
from utils import is_blank


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

    created_at = fields.DateTime(dump_only=True)

    @validates("name")
    def validate_name(self, value):
        min_length = 3

        if is_blank(value) or len(value) < min_length:
            raise ValidationError(f"Product's name must be at least {min_length} characters long.")
