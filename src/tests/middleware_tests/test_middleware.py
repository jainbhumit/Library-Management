import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, g
from src.app.middleware.middleware import auth_middleware
from src.app.config.messages import *
from src.app.config.enumeration import Status
import jwt

# Set up a Flask app for testing
app = Flask(__name__)

class TestAuthMiddleware(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('src.app.utils.utils.Utils.decode_jwt_token')
    def test_missing_authorization_header(self, mock_decode):
        with app.test_request_context('/some/protected/route'):
            response, status_code = auth_middleware()
            self.assertEqual(status_code, 401)
            self.assertEqual(response['message'], MISSING_OR_INVALID_TOKEN)

    @patch('src.app.utils.utils.Utils.decode_jwt_token')
    def test_invalid_token_format(self, mock_decode):
        with app.test_request_context(
            '/some/protected/route', headers={'Authorization': 'InvalidTokenFormat'}
        ):
            response, status_code = auth_middleware()
            self.assertEqual(status_code, 401)
            self.assertEqual(response['message'], MISSING_OR_INVALID_TOKEN)

    @patch('src.app.utils.utils.Utils.decode_jwt_token')
    def test_expired_token(self, mock_decode):
        mock_decode.side_effect = jwt.ExpiredSignatureError
        with app.test_request_context(
            '/some/protected/route', headers={'Authorization': 'Bearer expired.token.here'}
        ):
            response, status_code = auth_middleware()
            self.assertEqual(status_code, 401)
            self.assertEqual(response['message'], TOKEN_EXPIRE)

    @patch('src.app.utils.utils.Utils.decode_jwt_token')
    def test_invalid_token(self, mock_decode):
        mock_decode.side_effect = jwt.InvalidTokenError
        with app.test_request_context(
            '/some/protected/route', headers={'Authorization': 'Bearer invalid.token.here'}
        ):
            response, status_code = auth_middleware()
            self.assertEqual(status_code, 401)
            self.assertEqual(response['message'], INVALID_TOKEN)

    @patch('src.app.utils.utils.Utils.decode_jwt_token')
    def test_valid_token(self, mock_decode):
        mock_decode.return_value = {"user_id": "12345", "role": "admin"}
        with app.test_request_context(
            '/some/protected/route', headers={'Authorization': 'Bearer valid.token.here'}
        ):
            auth_middleware()
            self.assertEqual(g.user_id, "12345")
            self.assertEqual(g.role, "admin")
