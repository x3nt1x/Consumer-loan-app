from app.models.loan import Loan
from marshmallow import Schema, fields, post_load


class LoanSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    interest_rate = fields.Int(required=True)
    submitted = fields.Date(required=True)
    term = fields.Date(required=True)
    borrower_id = fields.Int(required=True)

    @post_load
    def make_object(self, data):
        return Loan(**data)


loan_schema = LoanSchema()
