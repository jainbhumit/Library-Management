import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify, g
from src.app.controller.book.handler import BookHandler
from src.app.services.book_service import BookService
from src.app.model.books import Books
from src.app.config.enumeration import Status
from src.app.config.messages import *
from src.app.utils.utils import Utils

class TestBookHandler(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        # Mock the BookService
        self.mock_book_service = MagicMock(spec=BookService)
        self.book_handler = BookHandler.create(self.mock_book_service)

        # patch("src.app.utils.utils.Utils.admin", lambda *x,**y:lambda f:f).start()

        # Set up test data
        self.test_book = Books(id=1, title="Test Book", author="Test Author",no_of_copies="5",no_of_available="3")
        self.valid_create_payload = {
            "title": "Test Book",
            "author": "Test Author"
        }
        self.valid_update_payload = {
            "book_id": "1",
            "title": "Updated Book",
            "author": "Updated Author"
        }

    def test_create_book_success(self):
        """Test successful creation of a book."""
        with self.app.test_request_context(
            method='POST',
            json=self.valid_create_payload
        ):
            self.mock_book_service.add_book.return_value = None
            g.role = "admin"
            response, status_code = self.book_handler.create_book()
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {
                "status": Status.SUCCESS.value,
                "message": BOOK_ADD_SUCCESSFULLY,
            })

    def test_create_book_validation_error(self):
        """Test book creation with invalid payload."""
        with self.app.test_request_context(
            method='POST',
            json={}  # Invalid payload
        ):
            g.role = "admin"
            response, status_code = self.book_handler.create_book()
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], INVALID_REQUEST_BODY)

    def test_get_all_books(self):
        """Test fetching all books."""
        with self.app.test_request_context():
            self.mock_book_service.get_all_books.return_value = [self.test_book]

            response, status_code = self.book_handler.get_all_books()
            self.assertEqual(status_code, 200)
            # self.assertDictEqual(response["data"][0], self.test_book.__dict__)
            self.assertEqual(response["data"], [self.test_book.__dict__])

    def test_get_book_by_title(self):
        """Test fetching a book by title."""
        with self.app.test_request_context(
            query_string={"title": "Test Book"}
        ):
            self.mock_book_service.get_book_by_title.return_value = self.test_book

            response, status_code = self.book_handler.get_all_books()
            self.assertEqual(status_code, 200)

            self.assertEqual(response["data"], self.test_book.__dict__)

    def test_update_book_success(self):
        """Test successful update of a book."""
        with self.app.test_request_context(
            method='PUT',
            json=self.valid_update_payload
        ):
            self.mock_book_service.update_book_by_id.return_value = None
            g.role = "admin"

            response, status_code = self.book_handler.update_book()
            self.assertEqual(status_code, 200)
            self.assertEqual(response["message"], BOOK_UPDATE_SUCCESSFULLY)

    def test_remove_book_success(self):
        """Test successful removal of a book."""
        with self.app.test_request_context():
            self.mock_book_service.remove_book_by_id.return_value = None
            g.role = "admin"

            response, status_code = self.book_handler.remove_book(1)
            self.assertEqual(status_code, 200)
            self.assertEqual(response["message"], BOOK_DELETE_SUCCESSFULLY)

    def test_delete_all_books_success(self):
        """Test successful deletion of all books."""
        with self.app.test_request_context():
            self.mock_book_service.remove_all_book_by_id.return_value = None
            g.role = "admin"

            response, status_code = self.book_handler.delete_book(1)
            self.assertEqual(status_code, 200)
            self.assertEqual(response["message"], BOOK_DELETE_SUCCESSFULLY)

    def test_unexpected_error(self):
        """Test handling of unexpected errors."""
        with self.app.test_request_context():
            self.mock_book_service.get_all_books.side_effect = Exception("Unexpected error")

            response, status_code = self.book_handler.get_all_books()
            self.assertEqual(status_code, 500)
            self.assertEqual(response["message"], "Unexpected error")


