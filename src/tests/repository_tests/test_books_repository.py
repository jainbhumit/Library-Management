import unittest
from unittest.mock import MagicMock, patch
from src.app.repositories.books_repository import BooksRepository
from src.app.model.books import Books
from src.app.utils.errors.error import DatabaseError


class TestBooksRepository(unittest.TestCase):

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

        # Initialize BooksRepository with mocked DB
        self.books_repository = BooksRepository(self.mock_db)

    def test_add_book_success(self):
        # Arrange
        book = Books(id="1", title="Book Title", author="Author Name", no_of_copies=10, no_of_available=8)
        query = "INSERT INTO book ..."
        values = {"id": "1", "title": "Book Title", "author": "Author Name", "number_of_copies": 10,
                  "number_of_available_books": 8}
        self.mock_query_builder.insert.return_value = (query, values)

        # Act
        self.books_repository.add_book(book)

        # Assert
        self.mock_conn.execute.assert_called_once()

    def test_add_book_raises_database_error(self):
        # Arrange
        book = Books(id="1", title="Book Title", author="Author Name", no_of_copies=10, no_of_available=8)
        self.mock_conn.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.books_repository.add_book(book)

        self.assertEqual(str(context.exception), "Database error")

    def test_update_book_success(self):
        # Arrange
        book = Books(id="1", title="Updated Title", author="Updated Author", no_of_copies=10, no_of_available=8)
        query = "UPDATE book ..."
        values = {"title": "Updated Title", "author": "Updated Author", "id": "1"}
        self.mock_query_builder.update.return_value = (query, values)

        # Act
        self.books_repository.update_book(book)

        # Assert
        self.mock_cursor.execute.assert_called_once()

    def test_update_book_raises_database_error(self):
        # Arrange
        book = Books(id="1", title="Updated Title", author="Updated Author", no_of_copies=10, no_of_available=8)
        self.mock_cursor.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.books_repository.update_book(book)

        self.assertEqual(str(context.exception), "Database error")

    def test_delete_book_success(self):
        # Arrange
        book_id = "1"
        query = "DELETE FROM book ..."
        values = {"id": book_id}
        self.mock_query_builder.delete.return_value = (query, values)

        # Act
        self.books_repository.delete_book(book_id)

        # Assert
        self.mock_conn.execute.assert_called_once()

    def test_delete_book_raises_database_error(self):
        # Arrange
        book_id = "1"
        self.mock_conn.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.books_repository.delete_book(book_id)

        self.assertEqual(str(context.exception), "Database error")

    def test_get_books_success(self):
        # Arrange
        query = "SELECT ..."
        values = []
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchall.return_value = [
            ("1", "Book 1", "Author 1", 10, 8),
            ("2", "Book 2", "Author 2", 5, 2),
        ]

        # Act
        books = self.books_repository.get_books()

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Book 1")

    def test_get_books_empty(self):
        # Arrange
        query = "SELECT ..."
        values = []
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchall.return_value = []

        # Act
        books = self.books_repository.get_books()

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(len(books), 0)

    def test_get_book_by_title_success(self):
        # Arrange
        title = "Book 1"
        query = "SELECT ..."
        values = {"title": title}
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchone.return_value = ("1", "Book 1", "Author 1", 10, 8)

        # Act
        book = self.books_repository.get_book_by_title(title)

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Book 1")

    def test_get_book_by_title_not_found(self):
        # Arrange
        title = "Unknown Title"
        query = "SELECT ..."
        values = {"title": title}
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchone.return_value = None

        # Act
        book = self.books_repository.get_book_by_title(title)

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertIsNone(book)

    def test_update_book_availability_success(self):
        # Arrange
        book = Books(id="1", title="Book 1", author="Author 1", no_of_copies=12, no_of_available=10)
        query = "UPDATE book ..."
        values = {"number_of_copies": 12, "number_of_available_books": 10, "title": "Book 1"}
        self.mock_query_builder.update.return_value = (query, values)

        # Act
        self.books_repository.update_book_availability(book)

        # Assert
        self.mock_conn.execute.assert_called_once()

    def test_update_book_availability_raises_database_error(self):
        # Arrange
        book = Books(id="1", title="Book 1", author="Author 1", no_of_copies=12, no_of_available=10)
        self.mock_conn.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.books_repository.update_book_availability(book)

        self.assertEqual(str(context.exception), "Database error")

    def test_get_book_by_id_success(self):
        # Arrange
        book_id = "1"
        query = "SELECT ..."
        values = {"id": book_id}
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchone.return_value = ("1", "Book 1", "Author 1", 10, 8)

        # Act
        book = self.books_repository.get_book_by_id(book_id)

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertIsNotNone(book)
        self.assertEqual(book.id, "1")

    def test_get_book_by_id_not_found(self):
        # Arrange
        book_id = "999"
        query = "SELECT ..."
        values = {"id": book_id}
        self.mock_query_builder.select.return_value = (query, values)
        self.mock_cursor.fetchone.return_value = None

        # Act
        book = self.books_repository.get_book_by_id(book_id)

        # Assert
        self.mock_cursor.execute.assert_called_once()
        self.assertIsNone(book)


