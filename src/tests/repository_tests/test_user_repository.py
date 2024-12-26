import unittest
from unittest.mock import MagicMock, patch
from src.app.repositories.user_repository import UserRepository
from src.app.model.user import User
from src.app.utils.errors.error import DatabaseError


class TestUserRepository(unittest.TestCase):

    @patch("src.app.utils.db.db.DB")
    def setUp(self,mock_db):
        # Initialize mocked DB and QueryBuilder
        self.mock_db = mock_db

        # Mock DB connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db.get_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Initialize UserRepository with mocked DB
        self.user_repository = UserRepository(self.mock_db)
        pass

    @patch("src.app.repositories.user_repository.GenericQueryBuilder.insert")  # Mock the QueryBuilder
    def test_save_user_success(self,mock_query_builder):
        mock_conn = MagicMock()  # Mock DB connection
        self.mock_db.get_connection.return_value = mock_conn  # Return mock connection

        # Mock the insert method to return query and values
        mock_query_builder.return_value = (
            "INSERT INTO user ...",
            ("1", "John Doe", "john.doe@example.com", "Admin", 2024, "CS", "password"),
        )


        user = User(
            id="1",
            name="John Doe",
            email="john.doe@example.com",
            role="Admin",
            year=2024,
            branch="CS",
            password="password"
        )

        # Act
        self.user_repository.save_user(user)

        # Assert
        mock_query_builder.assert_called_once_with("user", {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "year": user.year,
            "branch": user.branch,
            "password": user.password
        })
        mock_conn.execute.assert_called_once_with(
            "INSERT INTO user ...",
            ("1", "John Doe", "john.doe@example.com", "Admin", 2024, "CS", "password"),
        )

    @patch("src.app.repositories.user_repository.GenericQueryBuilder.select")  # Mock the QueryBuilder
    def test_fetch_user_by_email_success(self,mock_query_builder):
        # Arrange
        email = "john.doe@example.com"
        query = "SELECT id, name, role, year, branch, email, password FROM user WHERE email = ?"
        values = [email,]
        mock_query_builder.return_value = (query, values)

        # Mock cursor.fetchone to return a user row
        self.mock_cursor.fetchone.return_value = ("1", "John Doe", "Admin", 2024, "CS", "john.doe@example.com", "securepassword")

        # Act
        user = self.user_repository.fetch_user_by_email(email)

        # Assert
        mock_query_builder.assert_called_once()
        self.mock_cursor.execute.assert_called_once_with(query,values)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, "1")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, email)

    @patch("src.app.repositories.user_repository.GenericQueryBuilder.select")  # Mock the QueryBuilder
    def test_fetch_user_by_email_not_found(self,mock_query_builder):
        # Arrange
        email = "unknown@example.com"
        query = "SELECT id, name, role, year, branch, email, password FROM user WHERE email = ?"
        values = [email,]
        mock_query_builder.return_value = (query, values)

        # Mock cursor.fetchone to return None
        self.mock_cursor.fetchone.return_value = None

        # Act
        user = self.user_repository.fetch_user_by_email(email)

        # Assert
        self.mock_cursor.execute.assert_called_once_with(query, values)
        self.assertIsNone(user)

    def test_save_user_raises_database_error(self):
        # Arrange
        user = User(
            id="1",
            name="John Doe",
            email="john.doe@example.com",
            role="Admin",
            year=2024,
            branch="CS",
            password="securepassword"
        )

        self.mock_conn.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.user_repository.save_user(user)

        self.assertEqual(str(context.exception), "Database error")

    def test_save_user_duplicate_entry_error(self):
        # Arrange
        user = User(
            id="1",
            name="John Doe",
            email="john.doe@example.com",
            role="Admin",
            year=2024,
            branch="CS",
            password="securepassword"
        )

        self.mock_conn.execute.side_effect = Exception("Duplicate entry")

        # Act & Assert
        with self.assertRaises(DatabaseError) as context:
            self.user_repository.save_user(user)

        self.assertEqual(str(context.exception), "Duplicate entry")

