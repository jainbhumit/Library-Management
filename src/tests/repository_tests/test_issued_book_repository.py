import unittest
from unittest.mock import MagicMock, patch
from src.app.repositories.issued_book_repository import IssuedBookRepository
from src.app.model.issued_books import IssuedBooks
from src.app.utils.errors.error import DatabaseError

class TestIssuedBookRepository(unittest.TestCase):

    @patch("src.app.utils.db.query.GenericQueryBuilder")
    @patch("src.app.utils.db.db.DB")
    def setUp(self, mock_db, mock_query_builder):
        # Mock DB and QueryBuilder
        self.mock_db = mock_db
        self.mock_query_builder = mock_query_builder

        # Mock DB connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db.get_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Initialize IssuedBookRepository with mocked DB
        self.issued_book_repository = IssuedBookRepository(self.mock_db)

    def test_save_issue_book_success(self):
        # Arrange
        issued_book = IssuedBooks(id="1", user_id="101", book_id="202", borrow_date="2023-01-01", return_date="2023-01-15")
        query = "INSERT INTO issuedBook ..."
        values = {
            "id": "1",
            "user_id": "101",
            "book_id": "202",
            "borrow_date": "2023-01-01",
            "return_date": "2023-01-15",
        }
        self.mock_query_builder.insert.return_value = (query, values)

        # Act
        self.issued_book_repository.save_issue_book(issued_book)

        # Assert
        self.mock_conn.execute.assert_called_once()

    def test_save_issue_book_raises_database_error(self):
        # Arrange
        issued_book = IssuedBooks(id="1", user_id="101", book_id="202", borrow_date="2023-01-01", return_date="2023-01-15")
        self.mock_conn.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.issued_book_repository.save_issue_book(issued_book)

        self.assertEqual(str(context.exception), "Database error")

    def test_remove_issue_book_success(self):
        # Arrange
        user_id = "101"
        book_id = "202"
        query = "DELETE FROM issuedBook ..."
        values = {"user_id": user_id, "book_id": book_id}
        self.mock_query_builder.delete.return_value = (query, values)

        # Act
        self.issued_book_repository.remove_issue_book(user_id, book_id)

        # Assert
        self.mock_conn.execute.assert_called_once()

    def test_remove_issue_book_raises_database_error(self):
        # Arrange
        user_id = "101"
        book_id = "202"
        self.mock_conn.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.issued_book_repository.remove_issue_book(user_id, book_id)

        self.assertEqual(str(context.exception), "Database error")

    def test_get_issue_books_success(self):
        # Arrange
        query = "SELECT ..."
        values = []
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchall.return_value = [
            ("1", "101", "202", "2023-01-01", "2023-01-15"),
            ("2", "102", "203", "2023-02-01", "2023-02-15"),
        ]

        # Act
        issued_books = self.issued_book_repository.get_issue_books()

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(len(issued_books), 2)
        self.assertEqual(issued_books[0].user_id, "101")

    def test_get_issue_books_empty(self):
        # Arrange
        query = "SELECT ..."
        values = []
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchall.return_value = []

        # Act
        issued_books = self.issued_book_repository.get_issue_books()

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(len(issued_books), 0)

    def test_get_issue_book_by_user_id_success(self):
        # Arrange
        user_id = "101"
        query = "SELECT ..."
        values = {"user_id": user_id}
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchall.return_value = [
            ("1", "101", "202", "2023-01-01", "2023-01-15"),
        ]

        # Act
        issued_books = self.issued_book_repository.get_issue_book_by_user_id(user_id)

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(len(issued_books), 1)
        self.assertEqual(issued_books[0].book_id, "202")

    def test_get_issue_book_by_user_id_empty(self):
        # Arrange
        user_id = "101"
        query = "SELECT ..."
        values = {"user_id": user_id}
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchall.return_value = []

        # Act
        issued_books = self.issued_book_repository.get_issue_book_by_user_id(user_id)

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(len(issued_books), 0)

    def test_get_issue_books_error(self):
        self.mock_cursor.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.issued_book_repository.get_issue_books()

        self.assertEqual(str(context.exception), "Database error")
