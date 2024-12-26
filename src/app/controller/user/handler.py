from fastapi import HTTPException,Request
from dataclasses import dataclass

from starlette import status

from src.app.config.enumeration import Status
from src.app.config.messages import *
from src.app.config.custome_error_code import VALIDATION_FAILURE, UNEXPECTED_ERROR, INVALID_CREDENTIALS,ALREADY_EXISTS
from src.app.dto.user import LoginDTO, SignupDTO
from src.app.model.responses import Response, CustomErrorResponse
from src.app.model.user import User
from src.app.services.user_service import UserService
from src.app.utils.errors.error import UserExistsError
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.utils import Utils
from src.app.utils.validators.validators import Validators
from src.app.utils.logger.logger import Logger

@dataclass
class UserHandler:
    user_service: UserService
    logger = Logger()

    @classmethod
    def create(cls, user_service):
        return cls(user_service)

    @api_logger(logger)
    def login(self, request:Request,request_body: LoginDTO):
        try:
            email = request_body.email
            password = request_body.password.strip()

            # Call the service layer to authenticate the user
            user = self.user_service.login_user(email, password)
            if not user:
                return CustomErrorResponse.error_response(
                    Response.response(INCORRECT_EMAIL_PASSWORD,Status.FAIL.value,INVALID_CREDENTIALS),
                    401
                )

            # Generate token
            token = Utils.create_jwt_token(user.id, user.role)
            return Response.response(TOKEN_GENERATE_SUCCESSFULLY,Status.SUCCESS.value,data={'token': token, 'role': user.role})
        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR)
            )
        except Exception as e:
            self.logger.error(str(e))
            return CustomErrorResponse.error_response(
                Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR),
                500
            )
    @api_logger(logger)
    def signup(self,request:Request, request_body: SignupDTO):
        try:
            # Validate and process the input
            name = request_body.name.strip()
            email = str(request_body.email).strip().lower()
            password = request_body.password.strip()
            year = request_body.year.strip()
            branch = request_body.branch.strip()
            role = request_body.role.strip()

            # Create user
            user = User(name=name, email=email, password=password, year=year, branch=branch)

            self.user_service.signup_user(user)

            # Generate token
            token = Utils.create_jwt_token(user.id, user.role)

            return Response.response(
                message=TOKEN_GENERATE_SUCCESSFULLY,
                status=Status.SUCCESS.value,
                data={"token": token, "role": user.role}
            )
        except UserExistsError as e:
            return CustomErrorResponse.error_response(
                Response.response(str(e), Status.FAIL.value, ALREADY_EXISTS),
                200
            )
        except HTTPException as e:
            return CustomErrorResponse.error_response(
                Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR),
                500
            )
        except Exception as e:
            self.logger.error(str(e))
            return CustomErrorResponse.error_response(
                Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR),
                500
            )
