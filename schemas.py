from marshmallow import Schema, fields


class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    original_id = fields.Int(required=True)
    name = fields.Str(required=True)
    symbol = fields.Str(required=True)
    national_id = fields.Str(required=True)
    source = fields.Str(required=True)
    industry_name = fields.Str(required=True)
    group_name = fields.Str(required=True)
    in_market = fields.Bool(required=True)


class StatusSchema(Schema):
    id = fields.Int(dump_only=True)
    company_id = fields.Int(required=True)
    count = fields.Int(allow_none=True)
    number = fields.Int(allow_none=True)


class FinancialStatementItemSchema(Schema):
    id = fields.Int(dump_only=True)
    fetched_id = fields.Str()
    noavaran_id = fields.Int()
    level_order = fields.Int()
    title = fields.Str()
    financial_statement_item_id = fields.Str()
    amount = fields.Int()
    statement_type = fields.Str()


class FinancialStatementSchema(Schema):
    id = fields.Int(dump_only=True)
    company_id = fields.Int(required=True)
    period_end = fields.Date(required=True)
    fiscal_year_end = fields.Date(required=True)
    period_type = fields.Int(required=True)
    audited = fields.Bool(required=True)
    consolidated = fields.Bool(required=True)
    represented = fields.Bool(required=True)
    items = fields.Nested(FinancialStatementItemSchema, many=True)


class RatioCalculationSchema(Schema):
    id = fields.Int(dump_only=True)
    calculated_ratio = fields.Float(required=True)
    ratio_list_id = fields.Int(required=True)
    financial_statement_id = fields.Int(required=True)
    company_original_id = fields.Int(required=True)
    fiscal_year_end = fields.Date(required=True)
    ratioNameEng = fields.Str(required=True)
    ratioNamePer = fields.Str(required=True)


class RatioListSchema(Schema):
    id = fields.Int(dump_only=True)
    ratioNameEng = fields.Str(required=True)
    ratioNamePer = fields.Str(required=True)
    ratioSymbol = fields.Str(required=True)
