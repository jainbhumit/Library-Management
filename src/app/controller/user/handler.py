from flask import request, jsonify
from werkzeug.routing import ValidationError
from dataclasses import dataclass

from src.app.config.enumeration import Status
from src.app.config.messages import *
from src.app.config.custome_error_code import VALIDATION_FAILURE, UNEXPECTED_ERROR
from src.app.model.responses import Response
from src.app.model.user import User
from src.app.services.user_service import UserService
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
    def login(self):
        request_body = request.get_json()
        try:
            email = request_body['email'].strip().lower()
            if not Validators.is_email_valid(email):
                return  Response.response(EMAIL_IS_NOT_VALID,Status.FAIL.value,VALIDATION_FAILURE),422
            password = request_body['password'].strip()

            user = self.user_service.login_user(email, password)

            token = Utils.create_jwt_token(user.id, user.role)
            return Response.response(TOKEN_GENERATE_SUCCESSFULLY,Status.SUCCESS.value,data={'token': token, 'role': user.role}),200
        except Exception as e:
            return Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR),400

    @api_logger(logger)
    def signup(self):
        request_body = request.get_json()
        try:
            name = request_body['name'].strip()
            if not Validators.is_name_valid(name):
                return Response.response(NAME_NOT_VALID, Status.FAIL.value, VALIDATION_FAILURE), 422
            email = request_body['email'].strip().lower()
            if not Validators.is_email_valid(email):
                return Response.response(EMAIL_IS_NOT_VALID, Status.FAIL.value, VALIDATION_FAILURE), 422
            password = request_body['password'].strip()
            if not Validators.is_password_valid(password):
                return Response.response(PASSWORD_NOT_VALID, Status.FAIL.value, VALIDATION_FAILURE), 422
            year = request_body['year'].strip()
            if not Validators.is_year_valid(year):
                return Response.response(YEAR_NOT_VALID, Status.FAIL.value, VALIDATION_FAILURE), 422
            branch = request_body['branch'].strip()
            if not Validators.is_branch_valid(branch):
                return Response.response(BRANCH_NOT_VALID, Status.FAIL.value, VALIDATION_FAILURE), 422
            role = request_body['role'].strip()
            if not Validators.is_valid_role(role):
                return Response.response(ROLE_NOT_VALID, Status.FAIL.value, VALIDATION_FAILURE), 422

            user = User(name=name, email=email, password=password, year=year,branch=branch)

            self.user_service.signup_user(user)
            token = Utils.create_jwt_token(user.id, user.role)
            return Response.response(TOKEN_GENERATE_SUCCESSFULLY, Status.SUCCESS.value,
                                     data={'token': token, 'role': user.role}), 200


        except Exception as e:
            return Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR),400