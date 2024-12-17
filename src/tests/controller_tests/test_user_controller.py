import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, request
from src.app.controller.user.handler import UserHandler
from src.app.services.user_service import UserService
from src.app.model.user import User
from src.app.config.messages import *
from src.app.config.enumeration import Status
from src.app.utils.validators.validators import Validators


class TestUserHandler(unittest.TestCase):

    def setUp(self):
        # Initialize Flask app and test client
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        # Mock UserService
        self.mock_user_service = MagicMock(spec=UserService)
        self.user_handler = UserHandler.create(self.mock_user_service)

        # Test data
        self.valid_signup_payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "StrongPass123!",
            "year": "2023",
            "branch": "CSE",
            "role": "USER"
        }
        self.invalid_email_payload = {
            "name": "John Doe",
            "email": "invalid_email",
            "password": "StrongPass123!",
            "year": "2023",
            "branch": "CSE",
            "role": "USER"
        }
        self.valid_login_payload = {
            "email": "john.doe@example.com",
            "password": "StrongPass123!"
        }

        # Mock User object
        self.mock_user = User(
            name="John Doe",
            email="john.doe@example.com",
            password="StrongPass123!",
            year="2023",
            branch="CSE"
        )
        self.mock_user.id = "123"
        self.mock_user.role = "USER"

    @patch("src.app.utils.utils.Utils.create_jwt_token", return_value="mocked_jwt_token")
    def test_signup_success(self, mock_create_jwt_token):
        """Test successful signup."""
        with self.app.test_request_context(method="POST", json=self.valid_signup_payload):
            self.mock_user_service.signup_user.return_value = None

            response, status_code = self.user_handler.signup()
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json["message"], TOKEN_GENERATE_SUCCESSFULLY)
            self.assertEqual(response.json["data"]["token"], "mocked_jwt_token")

    def test_signup_invalid_email(self):
        """Test signup with invalid email."""
        with self.app.test_request_context(method="POST", json=self.invalid_email_payload):
            response, status_code = self.user_handler.signup()
            self.assertEqual(status_code, 422)
            self.assertEqual(response.json["message"], EMAIL_IS_NOT_VALID)

    @patch("src.app.utils.utils.Utils.create_jwt_token", return_value="mocked_jwt_token")
    def test_login_success(self, mock_create_jwt_token):
        """Test successful login."""
        with self.app.test_request_context(method="POST", json=self.valid_login_payload):
            self.mock_user_service.login_user.return_value = self.mock_user

            response, status_code = self.user_handler.login()
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json["message"], TOKEN_GENERATE_SUCCESSFULLY)
            self.assertEqual(response.json["data"]["token"], "mocked_jwt_token")
            self.assertEqual(response.json["data"]["role"], self.mock_user.role)

    def test_login_invalid_email(self):
        """Test login with invalid email."""
        invalid_login_payload = {
            "email": "invalid_email",
            "password": "StrongPass123!"
        }
        with self.app.test_request_context(method="POST", json=invalid_login_payload):
            response, status_code = self.user_handler.login()
            self.assertEqual(status_code, 422)
            self.assertEqual(response.json["message"], EMAIL_IS_NOT_VALID)

    def test_login_user_not_found(self):
        """Test login with user not found."""
        with self.app.test_request_context(method="POST", json=self.valid_login_payload):
            self.mock_user_service.login_user.side_effect = Exception(INCORRECT_EMAIL_PASSWORD)

            response, status_code = self.user_handler.login()
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json["message"], INCORRECT_EMAIL_PASSWORD)

    def test_signup_validation_failure(self):
        """Test signup with validation errors for other fields."""
        invalid_payload = {
            "name": "",
            "email": "john.doe@example.com",
            "password": "short",
            "year": "abcd",
            "branch": "",
            "role": "INVALID_ROLE"
        }
        with self.app.test_request_context(method="POST", json=invalid_payload):
            response, status_code = self.user_handler.signup()
            self.assertEqual(status_code, 422)
            self.assertEqual(response.json["message"], NAME_NOT_VALID)

    def test_signup_user_already_exists(self):
        """Test signup with a user that already exists."""
        with self.app.test_request_context(method="POST", json=self.valid_signup_payload):
            self.mock_user_service.signup_user.side_effect = Exception(USER_ALREADY_EXISTS)

            response, status_code = self.user_handler.signup()
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json["message"], USER_ALREADY_EXISTS)

    def test_signup_unexpected_error(self):
        """Test signup with an unexpected error."""
        with self.app.test_request_context(method="POST", json=self.valid_signup_payload):
            self.mock_user_service.signup_user.side_effect = Exception("Unexpected Error")

            response, status_code = self.user_handler.signup()
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json["message"], "Unexpected Error")

    def test_login_unexpected_error(self):
        """Test login with an unexpected error."""
        with self.app.test_request_context(method="POST", json=self.valid_login_payload):
            self.mock_user_service.login_user.side_effect = Exception("Unexpected Error")

            response, status_code = self.user_handler.login()
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json["message"], "Unexpected Error")


