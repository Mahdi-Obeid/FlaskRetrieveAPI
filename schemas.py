from marshmallow import Schema, fields


class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    symbol = fields.Str(required=True)
    national_id = fields.Str(required=True)
    source = fields.Str(required=True)
    industry_name = fields.Str(required=True)
    group_name = fields.Str(required=True)
    in_market = fields.Bool(required=True)
    count = fields.Int(allow_none=True)
    number = fields.Int(allow_none=True)
