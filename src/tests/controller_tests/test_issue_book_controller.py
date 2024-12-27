import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import Request
from datetime import datetime, timedelta

from src.app.controller.issue_book.handler import IssueBookHandler
from src.app.dto.issue_book import IssueBookDTO
from src.app.model.issued_books import IssuedBooks
from src.app.config.enumeration import Role, Status
from src.app.utils.errors.error import NotExistsError, InvalidOperationError
from src.app.config.messages import *
from src.app.config.custome_error_code import *
import json


@pytest.fixture
def mock_request():
    """Mock FastAPI request fixture"""
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

    request = Request(mock_scope, receive=mock_receive)
    request.state.user = {"user_id": "test-user-id", "role": Role.USER.value}
    return request


@pytest.fixture
def admin_request():
    """Mock FastAPI request fixture with admin role"""
    mock_scope = {
        "type": "http",
        "headers": [],
        "method": "GET",
        "path": "/",
        "query_string": b"user_id=test-user-id",  # Set query string in scope
        "client": ("127.0.0.1", 8000),
    }

    async def mock_receive():
        return {"type": "http.request", "body": b""}

    request = Request(mock_scope, receive=mock_receive)
    request.state.user = {"user_id": "admin-id", "role": Role.ADMIN.value}
    return request


@pytest.fixture
def admin_request_no_params():
    """Mock FastAPI request fixture with admin role and no query params"""
    mock_scope = {
        "type": "http",
        "headers": [],
        "method": "GET",
        "path": "/",
        "query_string": b"",
        "client": ("127.0.0.1", 8000),
    }

    async def mock_receive():
        return {"type": "http.request", "body": b""}

    request = Request(mock_scope, receive=mock_receive)
    request.state.user = {"user_id": "admin-id", "role": Role.ADMIN.value}
    return request


@pytest.fixture
def issue_book_dto():
    """Issue Book DTO fixture"""
    return IssueBookDTO(
        book_id="test-book-id",
        return_date=(datetime.now() + timedelta(days=14)).date()
    )


@pytest.fixture
def sample_issued_book():
    """Sample issued book fixture"""
    return IssuedBooks(
        id="test-issue-id",
        user_id="test-user-id",
        book_id="test-book-id",
        borrow_date=datetime.now().date(),
        return_date=(datetime.now() + timedelta(days=14)).date()
    )


class TestIssueBookHandler:
    def setup_method(self):
        """Setup method that runs before each test"""
        self.mock_service = Mock()
        self.handler = IssueBookHandler.create(self.mock_service)

    @pytest.mark.asyncio
    async def test_issue_book_success(self, mock_request, issue_book_dto):
        # Call handler
        response = await self.handler.issue_book_by_user(mock_request, issue_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_ISSUE_SUCCESSFULLY

        # Verify service called correctly
        self.mock_service.issue_book.assert_called_once()
        issued_book = self.mock_service.issue_book.call_args[0][0]
        assert issued_book.user_id == "test-user-id"
        assert issued_book.book_id == issue_book_dto.book_id

    @pytest.mark.asyncio
    async def test_issue_book_not_exists(self, mock_request, issue_book_dto):
        # Mock service error
        self.mock_service.issue_book.side_effect = NotExistsError("Book not found")

        response = await self.handler.issue_book_by_user(mock_request, issue_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            response_data = response

        assert response_data["error_code"] == NOT_EXISTS
        assert "Book not found" in response_data["message"]

    @pytest.mark.asyncio
    async def test_issue_book_unexpected_error(self, mock_request, issue_book_dto):
        self.mock_service.issue_book.side_effect = Exception
        response = await self.handler.issue_book_by_user(mock_request, issue_book_dto)
        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response
        assert response_data["error_code"] == UNEXPECTED_ERROR

    @pytest.mark.asyncio
    async def test_return_book_success(self, mock_request):
        book_id = "test-book-id"

        response = await self.handler.return_book_by_user(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == RETURN_SUCCESSFULLY

        self.mock_service.return_issue_book.assert_called_once_with("test-user-id", book_id)

    @pytest.mark.asyncio
    async def test_return_book_not_exists(self, mock_request):
        book_id = "test-book-id"
        self.mock_service.return_issue_book.side_effect = NotExistsError("Issue record not found")

        response = await self.handler.return_book_by_user(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            response_data = response

        assert response_data["error_code"] == NOT_EXISTS
        assert "Issue record not found" in response_data["message"]

    @pytest.mark.asyncio
    async def test_return_book_unexpected_error(self, mock_request):
        book_id = "test-book-id"
        self.mock_service.return_issue_book.side_effect = Exception
        response = await self.handler.return_book_by_user(book_id, mock_request)
        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response
        assert response_data["error_code"] == DB_ERROR

    @pytest.mark.asyncio
    async def test_get_issued_books_user(self, mock_request, sample_issued_book):
        self.mock_service.get_issue_book_by_user_id.return_value = [sample_issued_book]

        response = await self.handler.get_issued_books(mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == ISSUE_BOOK_FETCH_SUCCESSFULLY
        assert len(response_data["data"]) == 1
        assert response_data["data"][0]["book_id"] == sample_issued_book.book_id

    @pytest.mark.asyncio
    async def test_get_issued_books_admin_all(self, admin_request_no_params, sample_issued_book):
        self.mock_service.get_all_issued_books.return_value = [sample_issued_book]

        response = await self.handler.get_issued_books(admin_request_no_params)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert len(response_data["data"]) == 1
        assert response_data["data"][0]["book_id"] == sample_issued_book.book_id
    @pytest.mark.asyncio
    async def test_get_issued_books_admin_all_error(self, admin_request_no_params, sample_issued_book):
        self.mock_service.get_all_issued_books.return_value = Exception

        response = await self.handler.get_issued_books(admin_request_no_params)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
    @pytest.mark.asyncio
    async def test_get_issued_books_admin_by_user(self, admin_request, sample_issued_book):
        self.mock_service.get_issue_book_by_user_id.return_value = [sample_issued_book]

        response = await self.handler.get_issued_books(admin_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert len(response_data["data"]) == 1
        assert response_data["data"][0]["book_id"] == sample_issued_book.book_id


    @pytest.mark.asyncio
    async def test_get_issued_books_admin_by_user_error(self, admin_request, sample_issued_book):
        self.mock_service.get_issue_book_by_user_id.return_value = Exception

        response = await self.handler.get_issued_books(admin_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR

    @pytest.mark.asyncio
    async def test_invalid_operation(self, mock_request, issue_book_dto):
        self.mock_service.issue_book.side_effect = InvalidOperationError("Book already issued")

        response = await self.handler.issue_book_by_user(mock_request, issue_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            response_data = response

        assert response_data["error_code"] == NOT_EXISTS
        assert "Book already issued" in response_data["message"]

    @pytest.mark.asyncio
    async def test_unexpected_error(self, mock_request):
        self.mock_service.get_issue_book_by_user_id.side_effect = Exception("Unexpected error")

        response = await self.handler.get_issued_books(mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Unexpected error" in response_data["message"]
