import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import HTTPException, Request

from src.app.config.custome_error_code import UNEXPECTED_ERROR, ALREADY_EXISTS, INVALID_CREDENTIALS
from src.app.config.enumeration import Status
from src.app.controller.user.handler import UserHandler
from src.app.dto.user import LoginDTO, SignupDTO
from src.app.model.user import User
from src.app.utils.errors.error import UserExistsError
from src.app.config.messages import *


@pytest.fixture
def login_dto():
    """Login DTO fixture"""
    return LoginDTO(
        email="test@jecrc.ac.in",
        password="Test@123"
    )


@pytest.fixture
def signup_dto():
    """Signup DTO fixture"""
    return SignupDTO(
        name="Test User",
        email="test@jecrc.ac.in",
        password="Test@123",
        year="1st",
        branch="CS",
        role="user"
    )


@pytest.fixture
def sample_user():
    """Sample user fixture"""
    return User(
        name="Test User",
        email="test@jecrc.ac.in",
        password="hashedpassword",
        year="1st",
        branch="CS",
        role="user",
        id="550e8400-e29b-41d4-a716-446655440000"
    )


class TestUserHandler:
    def setup_method(self):
        """Setup method that runs before each test"""
        self.mock_user_service = Mock()
        self.user_handler = UserHandler.create(self.mock_user_service)

        # Create mock request
        mock_scope = {
            "type": "http",
            "headers": [],
            "method": "POST",
            "path": "/",
            "query_string": b"",
            "client": ("127.0.0.1", 8000),
        }

        async def mock_receive():
            return {"type": "http.request", "body": b""}

        self.mock_request = Request(mock_scope, receive=mock_receive)

    @pytest.mark.asyncio
    async def test_login_success(self, login_dto, sample_user):
        # Mock service layer response
        self.mock_user_service.login_user.return_value = sample_user

        # Call the handler
        response = await self.user_handler.login(self.mock_request, login_dto)

        # Verify response
        assert response["status"] == Status.SUCCESS.value
        assert response["message"] == TOKEN_GENERATE_SUCCESSFULLY
        assert "token" in response["data"]
        assert response["data"]["role"] == sample_user.role

        # Verify service was called correctly
        self.mock_user_service.login_user.assert_called_once_with(
            login_dto.email,
            login_dto.password.strip()
        )

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, login_dto):
        # Mock service layer response for invalid credentials
        self.mock_user_service.login_user.return_value = None

        # Call the handler
        response = await self.user_handler.login(self.mock_request, login_dto)

        # Verify response
        if hasattr(response, 'body'):
            # If it's a JSONResponse
            response_body = response.body.decode()
            import json
            response_data = json.loads(response_body)
            assert response.status_code == 401
        else:
            # If it's a dict
            response_data = response

        assert response_data["error_code"] == INVALID_CREDENTIALS
        assert response_data["message"] == INCORRECT_EMAIL_PASSWORD

    @pytest.mark.asyncio
    async def test_login_unexpected_error(self, login_dto):
        # Mock service layer error
        self.mock_user_service.login_user.side_effect = Exception("Unexpected error")

        # Call the handler
        response = await self.user_handler.login(self.mock_request, login_dto)

        if hasattr(response, 'body'):
            # If it's a JSONResponse
            response_body = response.body.decode()
            import json
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            # If it's a dict
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR

    @pytest.mark.asyncio
    async def test_signup_success(self, signup_dto):
        # Mock service layer response
        self.mock_user_service.signup_user.return_value = None

        # Call the handler
        response = await self.user_handler.signup(self.mock_request, signup_dto)

        # Verify response
        assert response["status"] == Status.SUCCESS.value
        assert response["message"] == TOKEN_GENERATE_SUCCESSFULLY
        assert "token" in response["data"]
        assert "role" in response["data"]

        # Verify service was called with correct user object
        called_user = self.mock_user_service.signup_user.call_args[0][0]
        assert called_user.name == signup_dto.name.strip()
        assert called_user.email == signup_dto.email.strip().lower()
        assert called_user.password == signup_dto.password.strip()
        assert called_user.year == signup_dto.year.strip()
        assert called_user.branch == signup_dto.branch.strip()

    @pytest.mark.asyncio
    async def test_signup_user_exists(self, signup_dto):
        # Mock service layer error for existing user
        self.mock_user_service.signup_user.side_effect = UserExistsError("User already exists")

        # Call the handler
        response = await self.user_handler.signup(self.mock_request, signup_dto)

        # Verify response
        if hasattr(response, 'body'):
            # If it's a JSONResponse
            response_body = response.body.decode()
            import json
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            # If it's a dict
            response_data = response

        assert response_data["error_code"] == ALREADY_EXISTS
        assert "User already exists" in response_data["message"]

    @pytest.mark.asyncio
    async def test_signup_unexpected_error(self, signup_dto):
        # Mock service layer error
        self.mock_user_service.signup_user.side_effect = Exception("Unexpected error")

        # Call the handler
        response = await self.user_handler.signup(self.mock_request, signup_dto)

        # Verify response
        if hasattr(response, 'body'):
            # If it's a JSONResponse
            response_body = response.body.decode()
            import json
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            # If it's a dict
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Unexpected error" in response_data["message"]