import unittest
from unittest.mock import MagicMock
from flask import Flask, g
from datetime import datetime
from src.app.controller.issue_book.handler import IssueBookHandler
from src.app.services.issue_book_service import IssueBookService
from src.app.model.issued_books import IssuedBooks
from src.app.config.messages import *
from src.app.config.enumeration import Status, Role


class TestIssueBookHandler(unittest.TestCase):

    def setUp(self):
        # Create a Flask app and test client
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        # Mock the IssueBookService
        self.mock_issue_book_service = MagicMock(spec=IssueBookService)
        self.issue_book_handler = IssueBookHandler.create(self.mock_issue_book_service)

        # Setup user info for g context
        self.user_id = "123"
        self.admin_role = Role.ADMIN.value
        self.user_role = Role.USER.value

        # Setup test data
        self.test_issued_book = IssuedBooks(
            user_id=self.user_id,
            book_id="456",
            borrow_date=datetime(2024, 1, 1),
            return_date=datetime(2024, 1, 15)
        )
        self.valid_issue_payload = {
            "book_id": "456",
            "return_date": "2024-01-15"
        }

    def mock_g_context(self, user_id=None, role=None):
        g.user_id = user_id
        g.role = role

    def test_issue_book_success(self):
        """Test successful book issue by a user."""
        with self.app.test_request_context(
            method='POST',
            json=self.valid_issue_payload
        ):
            self.mock_g_context(user_id=self.user_id, role=self.user_role)
            self.mock_issue_book_service.issue_book.return_value = None

            response, status_code = self.issue_book_handler.issue_book_by_user()
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {
                "status": Status.SUCCESS.value,
                "message": BOOK_ISSUE_SUCCESSFULLY,
            })

    def test_issue_book_invalid_token(self):
        """Test book issue with invalid token."""
        with self.app.test_request_context(method='POST', json=self.valid_issue_payload):
            self.mock_g_context(user_id=None, role=self.user_role)

            response, status_code = self.issue_book_handler.issue_book_by_user()
            self.assertEqual(status_code, 401)
            self.assertEqual(response["message"], INVALID_TOKEN)

    def test_issue_book_validation_error(self):
        """Test book issue with invalid payload."""
        with self.app.test_request_context(method='POST', json={}):  # Missing required fields
            self.mock_g_context(user_id=self.user_id, role=self.user_role)

            response, status_code = self.issue_book_handler.issue_book_by_user()
            self.assertEqual(status_code, 422)
            self.assertEqual(response["message"], INVALID_REQUEST_BODY)

    def test_return_book_success(self):
        """Test successful book return by a user."""
        with self.app.test_request_context():
            self.mock_g_context(user_id=self.user_id, role=self.user_role)
            self.mock_issue_book_service.return_issue_book.return_value = None

            response, status_code = self.issue_book_handler.return_book_by_user(book_id="456")
            self.assertEqual(status_code, 200)
            self.assertEqual(response["message"], RETURN_SUCCESSFULLY)

    def test_get_issued_books_user(self):
        """Test fetching issued books for a user."""
        with self.app.test_request_context():
            self.mock_g_context(user_id=self.user_id, role=self.user_role)
            self.mock_issue_book_service.get_issue_book_by_user_id.return_value = [self.test_issued_book]

            response, status_code = self.issue_book_handler.get_issued_books()
            self.assertEqual(status_code, 200)
            self.assertEqual(response["data"], [self.test_issued_book.__dict__])

    def test_get_issued_books_admin_with_user_id(self):
        """Test admin fetching issued books by a specific user ID."""
        with self.app.test_request_context(query_string={"user_id": self.user_id}):
            self.mock_g_context(role=self.admin_role)
            self.mock_issue_book_service.get_issue_book_by_user_id.return_value = [self.test_issued_book]

            response, status_code = self.issue_book_handler.get_issued_books()
            self.assertEqual(status_code, 200)
            self.assertEqual(response["data"], [self.test_issued_book.__dict__])

    def test_get_all_issued_books_admin(self):
        """Test admin fetching all issued books."""
        with self.app.test_request_context():
            self.mock_g_context(role=self.admin_role)
            self.mock_issue_book_service.get_all_issued_books.return_value = [self.test_issued_book]

            response, status_code = self.issue_book_handler.get_issued_books()
            self.assertEqual(status_code, 200)
            self.assertEqual(response["data"], [self.test_issued_book.__dict__])

    def test_get_issued_books_invalid_token(self):
        """Test fetching issued books with invalid token."""
        with self.app.test_request_context():
            self.mock_g_context(user_id=None, role=self.user_role)

            response, status_code = self.issue_book_handler.get_issued_books()
            self.assertEqual(status_code, 401)
            self.assertEqual(response["message"], INVALID_TOKEN)

    def test_unexpected_error(self):
        """Test handling of unexpected errors."""
        with self.app.test_request_context():
            self.mock_g_context(user_id=self.user_id, role=self.user_role)
            self.mock_issue_book_service.get_issue_book_by_user_id.side_effect = Exception("Unexpected error")

            response, status_code = self.issue_book_handler.get_issued_books()
            self.assertEqual(status_code, 500)
            self.assertEqual(response["message"], "Unexpected error")
