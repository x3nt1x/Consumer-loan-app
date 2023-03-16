from app import db
from datetime import datetime
from app.models.loan import Loan
from app.models.client import Client
from app.models.blacklist import Blacklist
from app.schemas.loan_schema import loan_schema
from flask import Blueprint, jsonify, request

bp = Blueprint('loan', __name__, url_prefix='/api/loan')


@bp.route('/<int:borrower_id>', methods=['GET'])
def get_loans_by_borrower(borrower_id):
    """Get all loans by borrower"""
    loans = Loan.query.filter_by(borrower_id=borrower_id).all()
    result = loan_schema.dump(loans, many=True)

    return jsonify(result.data)


@bp.route('/', methods=['POST'])
def create_loan():
    """Create new loan"""
    json_data = request.get_json()

    if not json_data:
        return "No data provided", 404

    # extract data
    amount = json_data["amount"]
    term = json_data["term"]
    first_name = json_data["first_name"]
    last_name = json_data["last_name"]
    personal_id = json_data["personal_id"]

    if Blacklist.query.filter_by(personal_id=personal_id).first():
        return "User is blacklisted", 200

    # existing or new borrower
    borrower = Client.query.filter_by(personal_id=personal_id).first()

    if borrower:
        if check_application(borrower):
            return "Too many applications in 24 hours", 200
    else:
        borrower = Client(first_name=first_name, last_name=last_name, personal_id=personal_id)
        db.session.add(borrower)
        db.session.flush()

    date = datetime.strptime(term, '%Y-%m-%d').date()
    new_loan = Loan(amount=amount, term=date, borrower_id=borrower.id)

    db.session.add(new_loan)
    db.session.commit()

    result = loan_schema.dump(Loan.query.get(new_loan.id))

    return result.data, 201


def check_application(borrower: Client) -> bool:
    """Check if user has made too many applications past 24 hours"""
    day_in_seconds = 86400  # 24 hours in seconds

    # get last 3 applications submitted by user
    last_applications = Loan.query.filter_by(borrower_id=borrower.id).order_by(Loan.id.desc()).limit(3).all()

    if len(last_applications) < 3:
        return False

    # get the third application from the last user entries
    application = last_applications[2].submitted

    time_passed = (datetime.now().replace(microsecond=0) - application).total_seconds()

    return time_passed < day_in_seconds
