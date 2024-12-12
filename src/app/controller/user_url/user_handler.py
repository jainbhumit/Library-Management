from flask import request, jsonify
from werkzeug.routing import ValidationError
from dataclasses import dataclass

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
                raise ValidationError('Email is not valid')
            password = request_body['password'].strip()

            user = self.user_service.login_user(email, password)

            token = Utils.create_jwt_token(user.id, user.role)
            return jsonify({'token': token, 'role': user.role}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    @api_logger(logger)
    def signup(self):
        request_body = request.get_json()
        try:
            name = request_body['name'].strip()
            if not Validators.is_name_valid(name):
                raise ValidationError('Name is not valid')
            email = request_body['email'].strip().lower()
            if not Validators.is_email_valid(email):
                raise ValidationError('Email is not valid')
            password = request_body['password'].strip()
            if not Validators.is_password_valid(password):
                raise ValidationError('Password is not valid')
            year = request_body['year'].strip()
            if not Validators.is_year_valid(year):
                raise ValidationError('Year is not valid')
            branch = request_body['branch'].strip()
            if not Validators.is_branch_valid(branch):
                raise ValidationError('Branch is not valid')
            role = request_body['role'].strip()
            if not Validators.is_valid_role(role):
                raise ValidationError('Invalid Role')

            user = User(name=name, email=email, password=password, year=year,branch=branch)

            self.user_service.signup_user(user)
            token = Utils.create_jwt_token(user.id, user.role)
            return jsonify({'token': token, 'role': user.role}), 200

        except Exception as e:
            return jsonify({"message": str(e)}), 400




