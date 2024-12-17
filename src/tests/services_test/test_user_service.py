import unittest
from unittest.mock import MagicMock, patch
from src.app.model.user import User
from src.app.services.user_service import UserService
from src.app.utils.errors.error import UserExistsError, InvalidCredentialsError


class TestUserService(unittest.TestCase):

    def setUp(self):
        # Mock the UserRepository and initialize UserService with it
        self.mock_user_repository = MagicMock()
        self.user_service = UserService(self.mock_user_repository)

    @patch("src.app.utils.utils.Utils.hash_password", return_value="hashed_password")
    def test_signup_user_successfully(self, mock_hash_password):
        # Arrange
        self.mock_user_repository.fetch_user_by_email.return_value = None  # No user exists
        user = User(
            id="1",
            name="John Doe",
            email="example@gmail.com",
            branch="IT",
            year="1st",
            password="password"
        )

        # Act
        self.user_service.signup_user(user)

        # Assert
        self.mock_user_repository.fetch_user_by_email.assert_called_once_with("example@gmail.com")
        mock_hash_password.assert_called_once_with("password")
        self.mock_user_repository.save_user.assert_called_once_with(user)
        self.assertEqual(user.password, "hashed_password")

    def test_signup_user_already_exists(self):
        # Arrange
        self.mock_user_repository.fetch_user_by_email.return_value = User(
            id="1",
            name="Existing User",
            email="example@gmail.com",
            branch="CS",
            year="2nd",
            password="existing_password"
        )
        user = User(
            id="2",
            name="John Doe",
            email="example@gmail.com",
            branch="IT",
            year="1st",
            password="password"
        )

        # Act & Assert
        with self.assertRaises(UserExistsError):
            self.user_service.signup_user(user)
        self.mock_user_repository.fetch_user_by_email.assert_called_once_with("example@gmail.com")
        self.mock_user_repository.save_user.assert_not_called()

    @patch("src.app.utils.utils.Utils.check_password", return_value=True)
    def test_login_user_successfully(self, mock_check_password):
        # Arrange
        user = User(
            id="1",
            name="John Doe",
            email="example@gmail.com",
            branch="IT",
            year="1st",
            password="hashed_password"
        )
        self.mock_user_repository.fetch_user_by_email.return_value = user

        # Act
        result = self.user_service.login_user("example@gmail.com", "password")

        # Assert
        self.mock_user_repository.fetch_user_by_email.assert_called_once_with("example@gmail.com")
        mock_check_password.assert_called_once_with("password", "hashed_password")
        self.assertEqual(result, user)

    @patch("src.app.utils.utils.Utils.check_password", return_value=False)
    def test_login_user_invalid_password(self, mock_check_password):
        # Arrange
        user = User(
            id="1",
            name="John Doe",
            email="example@gmail.com",
            branch="IT",
            year="1st",
            password="hashed_password"
        )
        self.mock_user_repository.fetch_user_by_email.return_value = user

        # Act & Assert
        with self.assertRaises(InvalidCredentialsError):
            self.user_service.login_user("example@gmail.com", "wrong_password")
        self.mock_user_repository.fetch_user_by_email.assert_called_once_with("example@gmail.com")
        mock_check_password.assert_called_once_with("wrong_password", "hashed_password")

    def test_login_user_not_found(self):
        # Arrange
        self.mock_user_repository.fetch_user_by_email.return_value = None  # No user found

        # Act & Assert
        with self.assertRaises(InvalidCredentialsError):
            self.user_service.login_user("nonexistent@example.com", "password")
        self.mock_user_repository.fetch_user_by_email.assert_called_once_with("nonexistent@example.com")



