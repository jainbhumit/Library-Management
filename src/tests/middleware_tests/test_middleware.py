import pytest
from fastapi import FastAPI, Request, HTTPException
from starlette.testclient import TestClient
from unittest.mock import patch, Mock
import jwt
import datetime

from src.app.config.enumeration import Status, Role
from src.app.middleware.middleware import AuthMiddleware
from src.app.config.messages import *
from src.app.config.custome_error_code import *

# Test app setup
app = FastAPI()
app.add_middleware(AuthMiddleware)


@app.get("/test-protected")
async def test_protected():
    return {"message": "success"}


@app.get("/user/login")
async def test_login():
    return {"message": "login success"}


@app.get("/user/signup")
async def test_signup():
    return {"message": "signup success"}


client = TestClient(app)


def create_token(user_id="test-user", role=Role.USER.value, expired=False):
    """Helper function to create JWT tokens for testing"""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expires in 1 hour
        "iat": datetime.datetime.utcnow(),  # Issued at
        "nbf": datetime.datetime.utcnow(),  # Not before
    }
    return jwt.encode(payload, "SECRET", algorithm="HS256")


class TestAuthMiddleware:
    def setup_method(self):
        """Setup method that runs before each test"""
        self.client = client

    def test_exempt_routes_login(self):
        """Test that login route is exempt from authentication"""
        response = self.client.get("/user/login")
        assert response.status_code == 200
        assert response.json() == {"message": "login success"}

    def test_exempt_routes_signup(self):
        """Test that signup route is exempt from authentication"""
        response = self.client.get("/user/signup")
        assert response.status_code == 200
        assert response.json() == {"message": "signup success"}

    def test_missing_auth_header(self):
        """Test request without Authorization header"""
        response = self.client.get("/test-protected")
        assert response.status_code == 401
        assert response.json()["message"] == MISSING_OR_INVALID_TOKEN
        assert response.json()["error_code"] == TOKEN_MISSING

    def test_invalid_auth_header_format(self):
        """Test request with invalid Authorization header format"""
        with pytest.raises(HTTPException) as e:
            self.client.get("/test-protected", headers={"Authorization": "Invalid-Format"})
            exception = e.value
            assert exception.status_code == 401
            assert exception["message"] == MISSING_OR_INVALID_TOKEN
            assert exception["error_code"] == TOKEN_MISSING

    def test_valid_token(self):
        """Test request with valid token"""
        token = create_token()
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "success"}

    def test_expired_token(self):
        """Test request with expired token"""
        token = create_token(expired=True)
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401
        assert response.json()["message"] == TOKEN_EXPIRE
        assert response.json()["error_code"] == TOKEN_EXPIRED

    def test_invalid_token(self):
        """Test request with invalid token"""
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401
        assert response.json()["message"] == INVALID_TOKEN
        assert response.json()["error_code"] == TOKEN_INVALID

    def test_missing_user_id_in_token(self):
        """Test token without user_id claim"""
        payload = {
            "role": Role.USER.value,
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, "your-secret-key", algorithm="HS256")
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401
        assert response.json()["message"] == INVALID_TOKEN
        assert response.json()["error_code"] == TOKEN_INVALID

    def test_missing_role_in_token(self):
        """Test token without role claim"""
        payload = {
            "user_id": "test-user",
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, "your-secret-key", algorithm="HS256")
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401
        assert response.json()["message"] == INVALID_TOKEN
        assert response.json()["error_code"] == TOKEN_INVALID

    @patch('src.app.utils.context.set_user_to_context')
    def test_user_context_setting(self, mock_set_context):
        """Test that user context is properly set"""
        token = create_token()
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        mock_set_context.assert_called_once()
        context_call = mock_set_context.call_args
        assert context_call[1]['user_data']['user_id'] == "test-user"
        assert context_call[1]['user_data']['role'] == Role.USER.value
        assert response.status_code == 200

    def test_different_user_roles(self):
        """Test authentication with different user roles"""
        # Test with admin role
        admin_token = create_token(role=Role.ADMIN.value)
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200

        # Test with user role
        user_token = create_token(role=Role.USER.value)
        response = self.client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 200