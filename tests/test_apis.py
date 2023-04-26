import time
import unittest
import json
from auth.app import db
from auth.models import *
from tests.base import TestCaseBase
from tests.api_base import TestAPIBase

class TestAuthAPIs(TestCaseBase, TestAPIBase):
    """Test cases for auth APIs
    """
    def test_signup__valid_case(self):
        """Tests signup flow when all conditions are met.
        """
        response = self.signup_client(email="user1@test.com", password="abc123", name="user1")

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'User signed up successful.')
        self.assertIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 3)

    def test_signup__user_already_signedup(self):
        """Tests signup flow when user is already registered.
        """
        _ = self.signup_client(email="user1@test.com", password="abc123", name="user1")
        response = self.signup_client(email="user1@test.com", password="abc123", name="user1")

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
        response = self.signup_client(email="user1@test.com", password="abc123", name=None)

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertEqual(body['status'], 'failed')
        self.assertEqual(body['message'], 'Internal Error')
        self.assertNotIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 2)

    