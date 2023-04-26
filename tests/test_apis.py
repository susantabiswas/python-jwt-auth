import time
import unittest
import json
from auth.app import db
from tests.base import TestCaseBase
from tests.api_base import TestAPIBase
from auth.models.user import User
from auth.models.blocked_token import BlockedToken
from auth.api.auth_utils import *

class TestAuthAPIs(TestCaseBase, TestAPIBase):
    """Test cases for auth APIs
    """

    ####################### /auth/signup API tests #############################
    def test_signup__valid_case(self):
        """Tests signup flow when all conditions are met.
        """
        response = self.signup_client(dict(email="user1@test.com", password="abc123", name="user1"))

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'User signed up successful.')
        self.assertIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 3)

    def test_signup__user_already_signedup(self):
        """Tests signup flow when user is already registered.
        """
        _ = self.signup_client(dict(email="user1@test.com", password="abc123", name="user1"))
        response = self.signup_client(dict(email="user1@test.com", password="abc123", name="user1"))

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'User already exists.')
        self.assertNotIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 2)

    def test_signup__required_fields_missing(self):
        """Tests signup flow when user's required fields are missing'.
        """
        response = self.client.post(
            '/auth/signup',
            data=json.dumps(dict(email="user1@test.com", password="abc123")),
            content_type='application/json'
        )

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'Required fields are missing.')
        self.assertNotIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 2)

    def test_signup__user_invalid_data(self):
        """Tests signup flow when one of the user field is not correct.
        """
        response = self.signup_client(dict(email="user1@test.com", password="abc123", name=None))

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'Internal Error')
        self.assertNotIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 2)


    ####################### /auth/login API tests #############################
    def test_login__missing_user(self):
        """Tests login api when the user is missing
        """
        response = self.login_client({'email':"userNotPresent@test.com", 'password': 'abc'})
        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'User not found')
        self.assertEqual(len(body.keys()), 2)

    def test_login__incorrect_password(self):
        """Tests login api when the password is incorrect
        """
        # create the user and then try to login with the same email but diff password
        pwd_hash = generate_password_hash('abc')
        user = User(email='user1@test.com', password=pwd_hash, name='user1')
        db.session.add(user)
        db.session.commit()

        response = self.login_client({'email':"user1@test.com", 'password':"incorrectPwd"})

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'Incorrect Password')
        self.assertEqual(len(body.keys()), 2)

    def test_login__correct_password(self):
        """Tests login api when the password is correct
        """
        # create the user and then try to login with the same email and password
        pwd_hash = generate_password_hash('abc123')
        user = User(email='user1@test.com', password=pwd_hash, name='user1')
        db.session.add(user)
        db.session.commit()

        response = self.login_client(dict(email="user1@test.com", password="abc123"))

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'User login successful.')
        self.assertEqual(len(body.keys()), 3)

    def test_login__required_fields_missing(self):
        """Tests login api when some of the required fields are missing
        """
        response = self.login_client(dict(email='user1@test.com'))

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'Email / Password missing')
        self.assertEqual(len(body.keys()), 2)

    ####################### /auth/logout API tests #############################
    def test_logout__invalid_jwt(self):
        """Tests logout api flow when an invalid jwt is passed
        """
        # first create an user and get the jwt generated for it
        pwd_hash = generate_password_hash('abc123')
        user = User(email='user1@test.com', password=pwd_hash, name='user1')
        db.session.add(user)
        db.session.commit()

        # generate jwt for it
        jwt_token = encode_jwt_token(user_id=user.id)
        response = self.logout_client(jwt_token=jwt_token+"incorrect")

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['status'], 'failed')
        self.assertIsNotNone(body['message'])
        self.assertEqual(len(body.keys()), 2)


    def test_logout__valid_jwt(self):
        """Tests logout api flow when a valid jwt is passed
        """
        # first create an user and get the jwt generated for it
        pwd_hash = generate_password_hash('abc123')
        user = User(email='user1@test.com', password=pwd_hash, name='user1')
        db.session.add(user)
        db.session.commit()

        # generate jwt for it
        jwt_token = encode_jwt_token(user_id=user.id)
        response = self.logout_client(jwt_token=jwt_token)

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'Logout Successful')
        self.assertEqual(len(body.keys()), 2)
    
    ####################### /auth/user API tests #############################
    def test_user__invalid_jwt(self):
        """Tests the user GET api flow when the jwt is invalid
        """
        # first create an user and get the jwt generated for it
        pwd_hash = generate_password_hash('abc123')
        user = User(email='user1@test.com', password=pwd_hash, name='user1')
        db.session.add(user)
        db.session.commit()

        # generate jwt for it
        jwt_token = encode_jwt_token(user_id=user.id)
        response = self.user_get_client(jwt_token=jwt_token+"incorrect")

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['status'], 'failed')
        self.assertIsNotNone(body['message'])
        self.assertEqual(len(body.keys()), 2)


    def test_user__user_not_found(self):
        """Tests the user GET api flow when the user doesn't exists
        """
        # generate a valid jwt
        jwt_token = encode_jwt_token(user_id="1")
        response = self.user_get_client(jwt_token=jwt_token)

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'User not found')
        self.assertEqual(len(body.keys()), 2)

    def test_user__valid_jwt(self):
        """Tests the user GET api flow when the jwt is valid
        """
        # first create an user and get the jwt generated for it
        pwd_hash = generate_password_hash('abc123')
        user = User(email='user1@test.com', password=pwd_hash, name='user1')
        db.session.add(user)
        db.session.commit()

        # generate jwt for it
        jwt_token = encode_jwt_token(user_id=user.id)
        response = self.user_get_client(jwt_token=jwt_token)

        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'Successfully fetched user details')
        self.assertEqual(len(body.keys()), 3)
        self.assertIsInstance(body['details'], dict)
        self.assertEqual(len(body['details'].keys()), 4)
        self.assertEqual(sorted(['email', 'name', 'admin', 'registered_on']),
            sorted(body['details'].keys()))
    