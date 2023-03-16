from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
import click
from flask.cli import with_appcontext
from sqlalchemy import event
from sqlalchemy.engine import Engine
from .models.loan import Loan
from .models.client import Client
from .models.blacklist import Blacklist
from . import db


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Force sqlite to enforce foreign keys, as it doesn't by default
    Source: https://stackoverflow.com/a/15542046
    """
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def create_db():
    db.drop_all()
    db.create_all()


def seed_db():
    db.session.add(Client(first_name="first1", last_name="last1", personal_id=123))
    db.session.add(Client(first_name="first2", last_name="last2", personal_id=456))
    db.session.add(Client(first_name="first3", last_name="last3", personal_id=789))

    db.session.add(Blacklist(personal_id=456))

    db.session.add(Loan(amount=100, term=datetime(2023, 9, 1).date(), borrower_id=1))
    db.session.add(Loan(amount=400, term=datetime(2024, 1, 20).date(), borrower_id=3))
    db.session.add(Loan(amount=800, term=datetime(2025, 5, 30).date(), borrower_id=1))

    db.session.commit()


@click.command('init-db')
@click.option("--seed", is_flag=True, show_default=True, default=False, help="Seed database with initial data.")
@with_appcontext
def init_db_command(seed):
    """Clear the existing data and create new tables."""
    create_db()

    if seed:
        seed_db()

    click.echo('Database initialized.')
