from marshmallow import validates, fields, ValidationError
from api.models import User
from utils import is_blank, is_valid_email
from app import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    created_at = fields.DateTime(dump_only=True)
    password = fields.String(load_only=True)

    @validates("name")
    def validate_name(self, value):
        min_length = 3

        if is_blank(value) or len(value) < min_length:
            raise ValidationError(f"Name must be at least {min_length} characters long.")

    @validates("email")
    def validate_email(self, value):
        if not is_valid_email(value):
            raise ValidationError("Invalid email format.")

    @validates("address")
    def validate_address(self, value):
        min_length = 5
        if is_blank(value) or len(value) < min_length:
            raise ValidationError(f"Address must be at least {min_length} characters long.")
