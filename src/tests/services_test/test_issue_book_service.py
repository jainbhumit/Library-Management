import unittest
from unittest.mock import MagicMock, patch
from src.app.services.issue_book_service import IssueBookService
from src.app.model.issued_books import IssuedBooks
from src.app.model.books import Books
from src.app.utils.errors.error import NotExistsError, InvalidOperationError


class TestIssueBookService(unittest.TestCase):

    def setUp(self):

        self.mock_issued_book_repository = MagicMock()
        self.mock_book_repository = MagicMock()

        self.issue_book_service = IssueBookService(self.mock_issued_book_repository, self.mock_book_repository)

    def test_get_all_issued_books(self):
        # Arrange
        expected_issued_books = [IssuedBooks(user_id="1", book_id="101",borrow_date="2024-12-20",id="id1",return_date="2024-12-30"), IssuedBooks(user_id="2", book_id="102",borrow_date="2024-12-20",id="id1",return_date="2024-12-30")]
        self.mock_issued_book_repository.get_issue_books.return_value = expected_issued_books

        # Act
        result = self.issue_book_service.get_all_issued_books()

        # Assert
        self.mock_issued_book_repository.get_issue_books.assert_called_once()
        self.assertEqual(result, expected_issued_books)

    def test_issue_book_successfully(self):
        # Arrange
        book = Books(id="101", title="Book Title", no_of_available=5,author="author1")
        issued_book = IssuedBooks(user_id="1", book_id=None,borrow_date="2024-12-20",id="id1",return_date="2024-12-30")
        self.mock_book_repository.get_book_by_id.return_value = book

        # Act
        self.issue_book_service.issue_book(issued_book, "101")

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_issued_book_repository.save_issue_book.assert_called_once_with(issued_book)
        self.mock_book_repository.update_book_availability.assert_called_once()
        self.assertEqual(issued_book.book_id, "101")
        self.assertEqual(book.no_of_available, 4)

    def test_issue_book_not_exists(self):
        # Arrange
        issued_book = IssuedBooks(user_id="1", book_id=None,borrow_date="2024-12-20",id="id1",return_date="2024-12-30")
        self.mock_book_repository.get_book_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(NotExistsError):
            self.issue_book_service.issue_book(issued_book, "101")
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_issued_book_repository.save_issue_book.assert_not_called()

    def test_issue_book_not_available(self):
        # Arrange
        book = Books(id="101", title="Book Title", no_of_available=0,author="author1")
        issued_book = IssuedBooks(user_id="1", book_id=None,borrow_date="2024-12-20",id="id1",return_date="2024-12-30")
        self.mock_book_repository.get_book_by_id.return_value = book

        # Act & Assert
        with self.assertRaises(InvalidOperationError):
            self.issue_book_service.issue_book(issued_book, "101")
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_issued_book_repository.save_issue_book.assert_not_called()

    def test_return_issue_book_successfully(self):
        # Arrange
        book = Books(id="101", title="Book Title", no_of_available=5,author="author1")
        self.mock_book_repository.get_book_by_id.return_value = book

        # Act
        self.issue_book_service.return_issue_book("1", "101")

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_book_repository.update_book_availability.assert_called_once()
        self.mock_issued_book_repository.remove_issue_book.assert_called_once_with("1", "101")
        self.assertEqual(book.no_of_available, 6)

    def test_return_issue_book_not_exists(self):
        # Arrange
        self.mock_book_repository.get_book_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(NotExistsError):
            self.issue_book_service.return_issue_book("1", "101")
        self.mock_book_repository.get_book_by_id.assert_called_once_with("101")
        self.mock_book_repository.update_book_availability.assert_not_called()
        self.mock_issued_book_repository.remove_issue_book.assert_not_called()

    def test_get_issue_book_by_user_id(self):
        # Arrange
        user_id = "1"
        expected_issued_books = [IssuedBooks(user_id="1", book_id="101",borrow_date="2024-12-20",id="id1",return_date="2024-12-30"), IssuedBooks(user_id="1", book_id="102",borrow_date="2024-12-20",id="id1",return_date="2024-12-30")]
        self.mock_issued_book_repository.get_issue_book_by_user_id.return_value = expected_issued_books

        # Act
        result = self.issue_book_service.get_issue_book_by_user_id(user_id)

        # Assert
        self.mock_issued_book_repository.get_issue_book_by_user_id.assert_called_once_with(user_id)
        self.assertEqual(result, expected_issued_books)
