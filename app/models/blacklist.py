from app import db


class Blacklist(db.Model):
    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    personal_id = db.Column(db.Integer, unique=True, nullable=False)
