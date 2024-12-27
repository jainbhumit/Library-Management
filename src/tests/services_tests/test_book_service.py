import unittest
from unittest.mock import MagicMock
from src.app.services.book_service import BookService
from src.app.model.books import Books
from src.app.utils.errors.error import NotExistsError
from src.app.config.messages import BOOK_NOT_EXIST


class TestBookService(unittest.TestCase):

    def setUp(self):
        # Mock the repository
        self.mock_book_repository = MagicMock()
        # Initialize the service with the mocked repository
        self.book_service = BookService(self.mock_book_repository)

    def test_add_book_new_book(self):
        # Arrange
        new_book = Books(id="101", title="New Book", no_of_available=1, no_of_copies=1,author="author1")
        self.mock_book_repository.get_book_by_title.return_value = None

        # Act
        self.book_service.add_book(new_book)

        # Assert
        self.mock_book_repository.get_book_by_title.assert_called_once_with("New Book")
        self.mock_book_repository.add_book.assert_called_once_with(new_book)
        self.mock_book_repository.update_book_availability.assert_not_called()

    def test_add_book_existing_book(self):
        # Arrange
        existing_book = Books(id="101", title="Existing Book", no_of_available=5, no_of_copies=5,author="author1")
        new_book = Books(id="101", title="Existing Book",author="author1")
        self.mock_book_repository.get_book_by_title.return_value = existing_book

        # Act
        self.book_service.add_book(new_book)

        # Assert
        self.mock_book_repository.get_book_by_title.assert_called_once_with("Existing Book")
        self.mock_book_repository.update_book_availability.assert_called_once()
        self.assertEqual(existing_book.no_of_available, 6)
        self.assertEqual(existing_book.no_of_copies, 6)

    def test_update_book_by_id_success(self):
        # Arrange
        updated_book = Books(id="101", title="Updated Book",author="author1")
        self.mock_book_repository.get_book_by_id.return_value = Books(id="101", title="Existing Book",author="author1")

        # Act
        self.book_service.update_book_by_id(updated_book, "101")

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_book_repository.update_book.assert_called_once_with(updated_book)

    def test_update_book_by_id_not_exist(self):
        # Arrange
        updated_book = Books(id="101", title="Updated Book",author="author1")
        self.mock_book_repository.get_book_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(NotExistsError) as context:
            self.book_service.update_book_by_id(updated_book, "101")
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.assertEqual(str(context.exception), BOOK_NOT_EXIST)
        self.mock_book_repository.update_book.assert_not_called()

    def test_remove_all_book_by_id_success(self):
        # Arrange
        self.mock_book_repository.get_book_by_id.return_value = Books(id="101", title="Book to Remove",author="author1")

        # Act
        self.book_service.remove_all_book_by_id("101")

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_book_repository.delete_book.assert_called_once_with("101")

    def test_remove_all_book_by_id_not_exist(self):
        # Arrange
        self.mock_book_repository.get_book_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(NotExistsError) as context:
            self.book_service.remove_all_book_by_id("101")
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.assertEqual(str(context.exception), BOOK_NOT_EXIST)
        self.mock_book_repository.delete_book.assert_not_called()

    def test_remove_book_by_id_success(self):
        # Arrange
        book = Books(id="101", title="Book to Remove", no_of_available=3, no_of_copies=3,author="author1")
        self.mock_book_repository.get_book_by_id.return_value = book

        # Act
        self.book_service.remove_book_by_id("101")

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_book_repository.update_book_availability.assert_called_once_with(book)
        self.assertEqual(book.no_of_available, 2)
        self.assertEqual(book.no_of_copies, 2)

    def test_remove_book_by_id_not_exist(self):
        # Arrange
        self.mock_book_repository.get_book_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(NotExistsError) as context:
            self.book_service.remove_book_by_id("101")
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.assertEqual(str(context.exception), BOOK_NOT_EXIST)
        self.mock_book_repository.update_book_availability.assert_not_called()

    def test_get_all_books(self):
        # Arrange
        expected_books = [
            Books(id="101", title="Book 1", no_of_available=5, no_of_copies=5,author="author1"),
            Books(id="102", title="Book 2", no_of_available=3, no_of_copies=3,author="author1"),
        ]
        self.mock_book_repository.get_books.return_value = expected_books

        # Act
        result = self.book_service.get_all_books()

        # Assert
        self.mock_book_repository.get_books.assert_called_once()
        self.assertEqual(result, expected_books)

    def test_get_book_by_title_success(self):
        # Arrange
        expected_book = Books(id="101", title="Existing Book", no_of_available=5, no_of_copies=5,author="author1")
        self.mock_book_repository.get_book_by_title.return_value = expected_book

        # Act
        result = self.book_service.get_book_by_title("Existing Book")

        # Assert
        self.mock_book_repository.get_book_by_title.assert_called_once_with("Existing Book")
        self.assertEqual(result, expected_book)

    def test_get_book_by_title_not_exist(self):
        # Arrange
        self.mock_book_repository.get_book_by_title.return_value = None

        # Act & Assert
        with self.assertRaises(NotExistsError) as context:
            self.book_service.get_book_by_title("Non-Existent Book")
        self.mock_book_repository.get_book_by_title.assert_called_once_with("Non-Existent Book")
        self.assertEqual(str(context.exception), BOOK_NOT_EXIST)


