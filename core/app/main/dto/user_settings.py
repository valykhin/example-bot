from marshmallow import Schema, fields


class UserSettingsDto(Schema):
    language_code = fields.String(allow_none=True, default='en')
    is_consent_accepted = fields.Boolean(allow_none=True, default=False)

    class Meta:
        strict = True


user_settings_dto = UserSettingsDto()
