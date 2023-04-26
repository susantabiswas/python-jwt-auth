from datetime import datetime

from auth.app import db


class BlockedToken(db.Model):
    """Represents the schema to save the blocked token related information.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blocked_on = db.Column(db.DateTime, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, token, token_expiry):
        """Creates a new instance of TokenBlockList

        Args:
            token (_type_): JWT token
        """
        self.token = token
        self.blocked_on = datetime.utcnow()
        self.expiry = token_expiry

    def __repr__(self):
        """String representation

        Returns:
            str: <id:, token: >
        """
        return '<Id: {}, Token: {}>'.format(self.id, self.token)
