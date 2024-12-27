import unittest
from unittest.mock import patch

import pytest
from fastapi import Request, HTTPException

from src.app.config.enumeration import Role
from src.app.utils.errors.error import CustomHTTPException
from src.app.utils.utils import Utils


class TestUtils(unittest.TestCase):
    def setUp(self):

        @Utils.admin
        def admin_only_function(request:Request):
            return True

        @Utils.user
        def user_only_function(request:Request):
            return True

        @Utils.admin
        def admin_only_function_without_request():
            return True

        @Utils.user
        def user_only_function_without_request():
            return True

        self.admin_only_function = admin_only_function
        self.user_only_function = user_only_function
        self.admin_only_function_without_request = admin_only_function_without_request
        self.user_only_function_without_request = user_only_function_without_request

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

    def test_admin_decorator_with_admin_role(self):
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }
        mock_request = Request(mock_scope)
        mock_request.state.user = {"role": "admin"}

        result = self.admin_only_function(mock_request)

        self.assertTrue(result)

    def test_admin_decorator_with_non_admin_role(self):
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }
        mock_request = Request(mock_scope)
        mock_request.state.user = {"role": "user"}
        with pytest.raises(CustomHTTPException) as e:
            self.admin_only_function(mock_request)
            exception =e.value
            self.assertEqual(exception["status_code"], 403)
            self.assertEqual(exception["message"], "Unauthorized: Admin role required")

    def test_admin_decorator_with_no_request_arg(self):
        with pytest.raises(CustomHTTPException) as e:
            self.admin_only_function_without_request()
            exception =e.value
            self.assertEqual(exception["status_code"], 401)
            self.assertEqual(exception["message"], "Request context not available")


    def test_user_decorator_with_user_role(self):
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }
        mock_request = Request(mock_scope)
        mock_request.state.user = {"role": "user"}

        result = self.user_only_function(mock_request)

        self.assertTrue(result)

    def test_user_decorator_with_non_user_role(self):
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }
        mock_request = Request(mock_scope)
        mock_request.state.user = {"role": "admin"}
        with pytest.raises(CustomHTTPException) as e:
            self.user_only_function(mock_request)
            exception = e.value
            self.assertEqual(exception["status_code"], 403)
            self.assertEqual(exception["message"], "Unauthorized: User role required")

    def test_user_decorator_with_no_request_arg(self):
        with pytest.raises(CustomHTTPException) as e:
            self.user_only_function_without_request()
            exception =e.value
            self.assertEqual(exception["status_code"], 401)
            self.assertEqual(exception["message"], "Request context not available")







