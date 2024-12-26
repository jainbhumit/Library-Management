import pytest
from unittest.mock import Mock
from fastapi import Request

from src.app.config.custome_error_code import UNEXPECTED_ERROR, NOT_EXISTS, DB_ERROR
from src.app.controller.book.handler import BookHandler
from src.app.dto.book import CreateBookDTO, UpdateBookDTO
from src.app.model.books import Books
from src.app.config.enumeration import Role, Status
from src.app.utils.errors.error import NotExistsError
from src.app.config.messages import *
import json

@pytest.fixture
def mock_request():
    """Mock FastAPI request fixture with admin role"""
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
    request.state.user = {"user_id": "admin-id", "role": Role.ADMIN.value}
    return request

@pytest.fixture
def mock_request_with_title():
    """Mock FastAPI request fixture with title query param"""
    mock_scope = {
        "type": "http",
        "headers": [],
        "method": "GET",
        "path": "/",
        "query_string": b"title=test-title",
        "client": ("127.0.0.1", 8000),
    }

    async def mock_receive():
        return {"type": "http.request", "body": b""}

    request = Request(mock_scope, receive=mock_receive)
    return request

@pytest.fixture
def create_book_dto():
    """Create Book DTO fixture"""
    return CreateBookDTO(
        title="Test Book",
        author="Test Author"
    )

@pytest.fixture
def update_book_dto():
    """Update Book DTO fixture"""
    return UpdateBookDTO(
        book_id="test-book-id",
        title="Updated Book",
        author="Updated Author"
    )

@pytest.fixture
def sample_book():
    """Sample book fixture"""
    return Books(
        id="test-book-id",
        title="Test Book",
        author="Test Author"
    )

class TestBookHandler:
    def setup_method(self):
        """Setup method that runs before each test"""
        self.mock_service = Mock()
        self.handler = BookHandler.create(self.mock_service)

    @pytest.mark.asyncio
    async def test_create_book_success(self, mock_request, create_book_dto):
        # Call handler
        response = await self.handler.create_book(mock_request, create_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_ADD_SUCCESSFULLY

        # Verify service called correctly
        self.mock_service.add_book.assert_called_once()
        book = self.mock_service.add_book.call_args[0][0]
        assert book.title == create_book_dto.title
        assert book.author == create_book_dto.author

    @pytest.mark.asyncio
    async def test_create_book_error(self, mock_request, create_book_dto):
        # Mock service error
        self.mock_service.add_book.side_effect = Exception("Database error")

        response = await self.handler.create_book(mock_request, create_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Database error" in response_data["message"]

    @pytest.mark.asyncio
    async def test_update_book_success(self, mock_request, update_book_dto):
        response = await self.handler.update_book(mock_request, update_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_UPDATE_SUCCESSFULLY

        self.mock_service.update_book_by_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_book_not_exists(self, mock_request, update_book_dto):
        self.mock_service.update_book_by_id.side_effect = NotExistsError("Book not found")

        response = await self.handler.update_book(mock_request, update_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            response_data = response

        assert response_data["error_code"] == NOT_EXISTS
        assert "Book not found" in response_data["message"]

    @pytest.mark.asyncio
    async def test_update_book_error(self, mock_request, update_book_dto):
        self.mock_service.update_book_by_id.side_effect = Exception("Database error")

        response = await self.handler.update_book(mock_request, update_book_dto)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Database error" in response_data["message"]

    @pytest.mark.asyncio
    async def test_remove_book_success(self, mock_request):
        book_id = "test-book-id"

        response = await self.handler.remove_book(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_DELETE_SUCCESSFULLY

        self.mock_service.remove_book_by_id.assert_called_once_with(book_id)

    @pytest.mark.asyncio
    async def test_remove_book_not_exists(self, mock_request):
        book_id = "test-book-id"
        self.mock_service.remove_book_by_id.side_effect = NotExistsError("Book not found")

        response = await self.handler.remove_book(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            response_data = response

        assert response_data["error_code"] == NOT_EXISTS
        assert "Book not found" in response_data["message"]

    @pytest.mark.asyncio
    async def test_remove_book_error(self, mock_request):
        book_id = "test-book-id"
        self.mock_service.remove_book_by_id.side_effect = Exception("Database error")

        response = await self.handler.remove_book(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == DB_ERROR
        assert "Database error" in response_data["message"]

    @pytest.mark.asyncio
    async def test_delete_book_success(self, mock_request):
        book_id = "test-book-id"

        response = await self.handler.delete_book(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_DELETE_SUCCESSFULLY

        self.mock_service.remove_all_book_by_id.assert_called_once_with(book_id)

    @pytest.mark.asyncio
    async def test_delete_book_not_exists(self, mock_request):
        book_id = "test-book-id"
        self.mock_service.remove_all_book_by_id.side_effect = NotExistsError("Book not found")

        response = await self.handler.delete_book(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 200
        else:
            response_data = response

        assert response_data["error_code"] == NOT_EXISTS
        assert "Book not found" in response_data["message"]

    @pytest.mark.asyncio
    async def test_delete_book_error(self, mock_request):
        book_id = "test-book-id"
        self.mock_service.remove_all_book_by_id.side_effect = Exception("Database error")

        response = await self.handler.delete_book(book_id, mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Database error" in response_data["message"]

    @pytest.mark.asyncio
    async def test_get_all_books_success(self, mock_request, sample_book):
        self.mock_service.get_all_books.return_value = [sample_book]

        response = await self.handler.get_all_books(mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_FETCH_SUCCESSFULLY
        assert len(response_data["data"]) == 1
        assert response_data["data"][0]["title"] == sample_book.title

    @pytest.mark.asyncio
    async def test_get_all_books_empty(self, mock_request):
        self.mock_service.get_all_books.return_value = []

        response = await self.handler.get_all_books(mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value

    @pytest.mark.asyncio
    async def test_get_all_books_error(self, mock_request):
        self.mock_service.get_all_books.side_effect = Exception("Database error")

        response = await self.handler.get_all_books(mock_request)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Database error" in response_data["message"]

    @pytest.mark.asyncio
    async def test_get_book_by_title_success(self, mock_request_with_title, sample_book):
        self.mock_service.get_book_by_title.return_value = sample_book

        response = await self.handler.get_all_books(mock_request_with_title)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value
        assert response_data["message"] == BOOK_FETCH_SUCCESSFULLY
        assert response_data["data"]["title"] == sample_book.title

    @pytest.mark.asyncio
    async def test_get_book_by_title_not_found(self, mock_request_with_title):
        self.mock_service.get_book_by_title.return_value = None

        response = await self.handler.get_all_books(mock_request_with_title)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
        else:
            response_data = response

        assert response_data["status"] == Status.SUCCESS.value

    @pytest.mark.asyncio
    async def test_get_book_by_title_error(self, mock_request_with_title):
        self.mock_service.get_book_by_title.side_effect = Exception("Database error")

        response = await self.handler.get_all_books(mock_request_with_title)

        if hasattr(response, 'body'):
            response_body = response.body.decode()
            response_data = json.loads(response_body)
            assert response.status_code == 500
        else:
            response_data = response

        assert response_data["error_code"] == UNEXPECTED_ERROR
        assert "Database error" in response_data["message"]