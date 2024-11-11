from config import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    symbol = db.Column(db.String(50))
    national_id = db.Column(db.String(50))
    source = db.Column(db.String(100))
    industry_name = db.Column(db.String(100))
    group_name = db.Column(db.String(100))
    in_market = db.Column(db.Boolean)
    count = db.Column(db.Integer())
    number = db.Column(db.Integer())