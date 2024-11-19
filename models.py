from config import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    symbol = db.Column(db.String(50))
    national_id = db.Column(db.String(50))
    source = db.Column(db.String(100))
    industry_name = db.Column(db.String(100))
    group_name = db.Column(db.String(100))
    in_market = db.Column(db.Boolean)
    # foreign key for Status
    status = db.relationship(
        "Status",
        backref="company",
        uselist=False,
    )
    # foreign key for Financial Statements
    financial_statements = db.relationship(
        "FinancialStatement",
        backref="company",
        lazy="dynamic",
    )


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_original_id = db.Column(
        db.Integer,
        db.ForeignKey("company.original_id"),
        unique=True,
        nullable=False,
    )
    count = db.Column(db.Integer())
    number = db.Column(db.Integer())


class FinancialStatement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company.original_id"),
    )
    period_end = db.Column(db.Date)
    fiscal_year_end = db.Column(db.Date)
    period_type = db.Column(
        db.Integer,
        info={"choices": [3, 6, 9, 12]},
    )
    audited = db.Column(db.Boolean, default=False)
    consolidated = db.Column(db.Boolean, default=False)
    represented = db.Column(db.Boolean, default=False)
    items = db.relationship(
        "FinancialStatementItem",
        backref="financial_statement",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # ensures that period_type only have the defined values
    __table_args__ = (db.CheckConstraint("period_type IN (3, 6, 9, 12)"),)


class FinancialStatementItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fetched_id = db.Column(db.String(50))
    noavaran_id = db.Column(db.Integer)
    level_order = db.Column(db.Integer)
    title = db.Column(db.String(200))
    financial_statement_item_id = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    statement_type = db.Column(db.String(50))
    financial_statement_id = db.Column(
        db.Integer,
        db.ForeignKey("financial_statement.id"),
    )
