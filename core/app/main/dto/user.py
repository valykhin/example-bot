from marshmallow import Schema, fields

from .user_settings import UserSettingsDto


class UserDto(Schema):
    id = fields.Integer()
    telegram_id = fields.Integer(allow_none=True)
    name = fields.String(allow_none=True)
    last_name = fields.String(allow_none=True)
    phone = fields.String(allow_none=True)
    email = fields.String(allow_none=True)
    settings = fields.Nested(UserSettingsDto(), allow_none=True)
    nickname = fields.String(allow_none=True)
    password = fields.String(load_only=True, allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)
    enabled = fields.Boolean(allow_none=True)

    class Meta:
        strict = True


user_dto = UserDto()
users_dto = UserDto(many=True)
