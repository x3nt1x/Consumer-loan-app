from app import db


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    personal_id = db.Column(db.Integer, unique=True, nullable=False)
