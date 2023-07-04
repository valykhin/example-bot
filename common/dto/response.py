from marshmallow import Schema, fields


class ErrorResponse(Schema):
    code = fields.Integer(allow_none=True)
    error_code = fields.String(allow_none=True)
    name = fields.String(allow_none=True)
    description = fields.String(allow_none=True)

    class Meta:
        strict = True


error_response_dto = ErrorResponse()
