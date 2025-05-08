from marshmallow import Schema, fields, post_load, ValidationError
from api.models import ResourceModel

class ResourceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_resource(self, data, **kwargs):
        return ResourceModel(**data)
    
    def validate_name(self, name):
        if not name.strip():
            raise ValidationError("Name cannot be empty.")
        if len(name) > 255:
            raise ValidationError("Name cannot be longer than 255 characters.")

    def validate_description(self, description):
        if not description.strip():
            raise ValidationError("Description cannot be empty.")
        if len(description) > 500:
            raise ValidationError("Description cannot be longer than 500 characters.")

    class Meta:
        strict = True
