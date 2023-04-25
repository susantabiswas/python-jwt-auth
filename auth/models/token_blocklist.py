
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TokenBlocklist(db.Model):
    """Represents the schema to save the blocked token related information.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blocked_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<id: {}, token: {}>'.format(id, self.token)