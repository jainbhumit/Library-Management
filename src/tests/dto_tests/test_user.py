import pytest
from src.app.dto.user import LoginDTO, SignupDTO
from src.app.utils.errors.error import CustomHTTPException
from src.app.config.messages import (
    EMAIL_IS_NOT_VALID, NAME_NOT_VALID, PASSWORD_NOT_VALID, YEAR_NOT_VALID,
    BRANCH_NOT_VALID, ROLE_NOT_VALID
)
from src.app.config.custome_error_code import VALIDATION_FAILURE


class TestLoginDTO:
    def test_valid_login_dto(self):
        # Valid LoginDTO data
        data = {"email": "user@jecrc.ac.in", "password": "Strongpass@123"}
        dto = LoginDTO(**data)
        assert dto.email == data["email"]
        assert dto.password == data["password"]

    def test_invalid_email_login_dto(self):
        # Invalid email for LoginDTO
        data = {"email": "user@gmail", "password": "Strongpass@123"}
        with pytest.raises(CustomHTTPException) as exc_info:
            LoginDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == EMAIL_IS_NOT_VALID


class TestSignupDTO:
    def test_valid_signup_dto(self):
        # Valid SignupDTO data
        data = {
            "name": "John Doe",
            "email": "john@jecrc.ac.in",
            "password": "Strongpass@123",
            "year": "1st",
            "branch": "IT",
            "role": "user",
        }
        dto = SignupDTO(**data)
        assert dto.name == data["name"]
        assert dto.email == data["email"]
        assert dto.password == data["password"]
        assert dto.year == data["year"]
        assert dto.branch == data["branch"]
        assert dto.role == data["role"]

    def test_invalid_name_signup_dto(self):
        # Invalid name for SignupDTO
        data = {
            "name": "1",  # Invalid name
            "email": "john@jecrc.ac.in",
            "password": "Strongpass@123",
            "year": "1st",
            "branch": "IT",
            "role": "user",
        }
        with pytest.raises(CustomHTTPException) as exc_info:
            SignupDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == NAME_NOT_VALID

    def test_invalid_password_signup_dto(self):
        # Invalid password for SignupDTO
        data = {
            "name": "John Doe",
            "email": "john@jecrc.ac.in",
            "password": "weak",  # Invalid password
            "year": "1st",
            "branch": "IT",
            "role": "user",
        }
        with pytest.raises(CustomHTTPException) as exc_info:
            SignupDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == PASSWORD_NOT_VALID

    def test_invalid_email_signup_dto(self):
        # Invalid email for SignupDTO
        data = {
            "name": "John Doe",
            "email": "invalid-email",  # Invalid email
            "password": "Strongpass@123",
            "year": "1st",
            "branch": "IT",
            "role": "user",
        }
        with pytest.raises(CustomHTTPException) as exc_info:
            SignupDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == EMAIL_IS_NOT_VALID

    def test_invalid_year_signup_dto(self):
        # Invalid year for SignupDTO
        data = {
            "name": "John Doe",
            "email": "john@jecrc.ac.in",
            "password": "Strongpass@123",
            "year": "5th",  # Invalid year
            "branch": "IT",
            "role": "user",
        }
        with pytest.raises(CustomHTTPException) as exc_info:
            SignupDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == YEAR_NOT_VALID

    def test_invalid_branch_signup_dto(self):
        # Invalid branch for SignupDTO
        data = {
            "name": "John Doe",
            "email": "john@jecrc.ac.in",
            "password": "Strongpass@123",
            "year": "1st",
            "branch": "INVALID",  # Invalid branch
            "role": "user",
        }
        with pytest.raises(CustomHTTPException) as exc_info:
            SignupDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == BRANCH_NOT_VALID

    def test_invalid_role_signup_dto(self):
        # Invalid role for SignupDTO
        data = {
            "name": "John Doe",
            "email": "john@jecrc.ac.in",
            "password": "Strongpass@123",
            "year": "1st",
            "branch": "IT",
            "role": "invalidrole",  # Invalid role
        }
        with pytest.raises(CustomHTTPException) as exc_info:
            SignupDTO(**data)

        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.error_code == VALIDATION_FAILURE
        assert exception.message == ROLE_NOT_VALID
