from auth.app import db
from auth.models.blocked_token import BlockedToken
from auth.models.user import User
from tests.base import TestCaseBase

class UserModelTest(TestCaseBase):
    def test_user_model(self):
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

class BlockedTokenModelTest(TestCaseBase):
    def test_user_model(self):
        blocked_token = BlockedToken(token="sadasdsadasd")
        db.session.add(blocked_token)
        db.session.commit()

        # retrieve the user
        retrieved_blocked_token = BlockedToken.query.filter_by(token=blocked_token.token).first()

        self.assertTrue(blocked_token.token, retrieved_blocked_token.token)
