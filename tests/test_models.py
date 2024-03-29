from auth.app import db
from auth.models.blocked_token import BlockedToken
from auth.models.user import User
from tests.base import TestCaseBase
from datetime import datetime
class UserModelTest(TestCaseBase):
    def test_user_model(self):
        """Tests the user model
        """
        user = User(email="user@test.com",
            password="test",
            name="user")
        db.session.add(user)
        db.session.commit()

        # retrieve the user
        retrieved_user = User.query.filter_by(email=user.email).first()

        self.assertTrue(user.email, retrieved_user.email)
        self.assertTrue(user.password, retrieved_user.password)
        self.assertTrue(user.name, retrieved_user.name)

    def test_user_repr(self):
        user = User(email="user@test.com",
            password="test",
            name="user")
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(
            user.__repr__(),
            '<Id: {}, Name: {}>'.format(user.id, user.name))



class BlockedTokenModelTest(TestCaseBase):
    def test_user_model(self):
        """Tests the BlockToken model
        """
        blocked_token = BlockedToken(token="sadasdsadasd", token_expiry=datetime.utcnow())
        db.session.add(blocked_token)
        db.session.commit()

        # retrieve the blocked token
        retrieved_blocked_token = BlockedToken.query.filter_by(token=blocked_token.token).first()

        self.assertTrue(blocked_token.token, retrieved_blocked_token.token)

    def test_user_repr(self):
        blocked_token = BlockedToken(token="sadasdsadasd", token_expiry=datetime.utcnow())
        db.session.add(blocked_token)
        db.session.commit()
        
        self.assertEqual(
            blocked_token.__repr__(),
            '<Id: {}, Token: {}>'.format(blocked_token.id, blocked_token.token))