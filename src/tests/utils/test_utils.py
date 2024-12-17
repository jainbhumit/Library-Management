import unittest
from unittest.mock import patch

from flask import Flask,g

from src.app.config.enumeration import Role
from src.app.utils.utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.app_context().push()

        @Utils.admin
        def admin_only_function(*args, **kwargs):
            return True

        @Utils.user
        def user_only_function(*args, **kwargs):
            return True

        self.admin_only_function = admin_only_function
        self.user_only_function = user_only_function

    def test_hash_password(self):
        password = "mypassword"
        hashed_password = Utils.hash_password(password)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(hashed_password.startswith("$2b$"))

    def test_check_password(self):
        password = "mypassword"
        hashed_password = Utils.hash_password(password)
        self.assertTrue(Utils.check_password(password, hashed_password))
        self.assertFalse(Utils.check_password("wrongpassword", hashed_password))

    def test_create_jwt_token(self):
        user_id = "12345"
        role = "admin"
        token = Utils.create_jwt_token(user_id, role)
        self.assertIsInstance(token, str)

    def test_decode_jwt_token(self):
        user_id = "12345"
        role = "admin"
        token = Utils.create_jwt_token(user_id, role)
        decoded_payload = Utils.decode_jwt_token(token)
        self.assertEqual(decoded_payload["user_id"], user_id)
        self.assertEqual(decoded_payload["role"], role)

    @patch("flask.g.get")
    def test_admin_decorator_with_admin_role(self, mock_g_get):
        mock_g_get.return_value = Role.ADMIN.value

        result = self.admin_only_function()

        self.assertEqual(result, True)

    @patch("flask.g.get")
    def test_admin_decorator_with_non_admin_role(self, mock_g_get):
        mock_g_get.return_value = Role.USER.value

        result, status_code = self.admin_only_function()

        self.assertEqual(status_code, 403)
        self.assertEqual(result.get_json(), {"message": "Unauthorized: Admin role required"})

    @patch("flask.g.get")
    def test_user_decorator_with_user_role(self, mock_g_get):
        mock_g_get.return_value = Role.USER.value

        result = self.user_only_function()

        self.assertEqual(result, True)

    @patch("flask.g.get")
    def test_user_decorator_with_non_user_role(self, mock_g_get):
        mock_g_get.return_value = Role.ADMIN.value

        result, status_code = self.user_only_function()

        self.assertEqual(status_code, 403)
        self.assertEqual(result.get_json(), {"message": "Unauthorized: User role required"})







