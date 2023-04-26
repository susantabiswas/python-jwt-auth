
from datetime import datetime

from auth.app import db


class User(db.Model):
    """Represents the User model database schema. Information related
    to the user is saved.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    registration_timestamp = db.Column(
        db.DateTime(timezone=False),
        nullable=False, default=datetime.utcnow())
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Id:{}, Name: {}>".format(id, self.name)
