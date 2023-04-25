from auth.app import db
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

