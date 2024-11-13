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
    # foriegn keys
    status = db.relationship(
        "Status",
        backref="company",
        uselist=False,
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
