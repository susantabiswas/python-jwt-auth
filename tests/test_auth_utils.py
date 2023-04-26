from auth.api.auth_utils import *
from tests.base import TestCaseBase
import jwt
import time
from auth.app import app

class TestAuthUtils(TestCaseBase):
    user_id = "1"

    def test_encode_jwt_token(self):
        # Test whether a valid jwt is generated
        jwt_token = encode_jwt_token(self.user_id)

        self.assertIsNotNone(jwt_token)
        self.assertIsInstance(jwt_token, str)

    def test_decode_jwt_token___valid_case(self):
        """Test whether a valid jwt token can be decoded
        """
        jwt_token = encode_jwt_token(self.user_id)
        decoded_user_id = decode_jwt_token(jwt_token=jwt_token)
        self.assertEqual(self.user_id, decoded_user_id)
        self.assertIsInstance(decoded_user_id, type(self.user_id))

    def test_decode_jwt_token__invalid_case(self):
        """Test whether an invalid jwt token can be decoded
        """
        jwt_token = encode_jwt_token(self.user_id)
        with self.assertRaises(jwt.InvalidTokenError):
            decode_jwt_token(jwt_token=jwt_token+"random")

    def test_decode_jwt_token__expired_token(self):
        """Test if an expired token can be decoded
        """
        jwt_token = encode_jwt_token(self.user_id)
        # Wait for the token to expire
        time.sleep(app.config['JWT_SECONDS'] + 1)

        with self.assertRaises(jwt.ExpiredSignatureError):
            decode_jwt_token(jwt_token)

    def test_create_response(self):
        """Test whether the response is created properly
        """
        response = create_response('failed', 'test message')
        self.assertIsInstance(response, dict)
        self.assertEqual(len(response.keys()), 2)
        self.assertIn('status', response)
        self.assertIn('message', response)

    def test_extract_jwt_token__valid_case(self):
        """Test if the jwt token can be extracted properly
        """
        headers = {
            'Authorization': 'Bearer <jwt_token>',
            'TestHeader': 'Dummy'
        }        
        jwt_token = extract_jwt_token(headers)
        self.assertIsNotNone(jwt_token)
        self.assertIsInstance(jwt_token, str)
        self.assertEqual(jwt_token, '<jwt_token>')

    def test_extract_jwt_token__missing_headers(self):
        """Test if the jwt token can be extracted when Authorization header is missing
        """
        headers = {
            'TestHeader': 'Dummy'
        }        
        jwt_token = extract_jwt_token(headers)
        self.assertIsNone(jwt_token)
         
    def test_block_jwt_token(self):
        """Test if a token can be blocked
        """
        jwt_token = encode_jwt_token(self.user_id)
        block_jwt_token(jwt_token)
        
        retrieved_token = BlockedToken.query.filter_by(token=jwt_token).first()
        self.assertEqual(jwt_token, retrieved_token.token)

    def test_is_jwt_blocked(self):
        """Test for blocked JWT token
        """
        blocked_jwt_token = encode_jwt_token(self.user_id)
        block_jwt_token(jwt_token=blocked_jwt_token)

        active_jwt_token = encode_jwt_token("2")
        # check if the blocked token is found to be blocked
        self.assertTrue(is_jwt_blocked(blocked_jwt_token))
        # Active JWT token should not be found as blocked
        self.assertFalse(is_jwt_blocked(active_jwt_token))

