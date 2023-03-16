from app import db
from datetime import datetime


class Loan(db.Model):
    __tablename__ = "loan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Integer, default=5)
    submitted = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    term = db.Column(db.Date, nullable=False)

    borrower = db.relationship("Client", backref=db.backref("client", lazy="dynamic"))
    borrower_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
