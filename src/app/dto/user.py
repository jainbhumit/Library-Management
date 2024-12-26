from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator
from starlette import status

from src.app.config.custome_error_code import VALIDATION_FAILURE
from src.app.config.enumeration import Status
from src.app.config.messages import EMAIL_IS_NOT_VALID, NAME_NOT_VALID, PASSWORD_NOT_VALID, YEAR_NOT_VALID, \
    BRANCH_NOT_VALID, ROLE_NOT_VALID
from src.app.model.responses import Response, CustomErrorResponse
from src.app.utils.errors.error import CustomHTTPException
from src.app.utils.validators.validators import Validators


class LoginDTO(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(v:str):

        if not Validators.is_email_valid(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,EMAIL_IS_NOT_VALID)
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@jecrc.ac.in",
                "password": "Strongpass@123"
            }
        }


class SignupDTO(BaseModel):
    name: str
    email: str
    password: str
    year: str
    branch: str
    role: str

    @field_validator('name')
    def validate_name(v:str):
        if not Validators.is_name_valid(v):

            raise CustomHTTPException(422,VALIDATION_FAILURE,NAME_NOT_VALID)
        return v

    @field_validator('password')
    def validate_password(v: str) -> str:
        if not Validators.is_password_valid(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,PASSWORD_NOT_VALID)
        return v

    @field_validator('email')
    def validate_email(v: str) -> str:
        if not Validators.is_email_valid(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,EMAIL_IS_NOT_VALID)
        return v

    @field_validator('year')
    def validate_year(v: str) -> str:
        if not Validators.is_year_valid(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,YEAR_NOT_VALID)

        return v

    @field_validator('branch')
    def validate_branch(v: str) -> str:
        if not Validators.is_branch_valid(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,BRANCH_NOT_VALID)

        return v

    @field_validator('role')
    def validate_role(v: str) -> str:
        if not Validators.is_valid_role(v):
            raise CustomHTTPException(422,VALIDATION_FAILURE,ROLE_NOT_VALID)

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@jecrc.ac.in.com",
                "password": "Strongpass@123",
                "year":"1st",
                "branch":"IT",
                "role":"user"

            }
        }