"""
opysnippets/marshmallow:1.0.0

Requirements
------------
marshmallow>=2.13.6,<3.0.0b0
"""
import datetime as dt

from marshmallow import fields, ValidationError

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class ODateTimeSchema(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return value.strftime(ISO_FORMAT)
        except (ValueError, AttributeError) as e:
            raise ValidationError(e) from None

    def _deserialize(self, value, attr, data):
        if value is None:
            return None
        if isinstance(value, dt.datetime):
            return value
        try:
            return dt.datetime.strptime(value, ISO_FORMAT)
        except ValueError as e:
            raise ValidationError(e) from None
