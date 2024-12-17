from dataclasses import dataclass

from flask import request, jsonify,g
from datetime import datetime

from pydantic import ValidationError

from src.app.config.custome_error_code import *
from src.app.config.messages import *
from src.app.dto.issue_book import IssueBookDTO
from src.app.model.issued_books import IssuedBooks
from src.app.model.responses import Response
from src.app.utils.errors.error import *
from src.app.services.issue_book_service import IssueBookService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.logger.logger import Logger
from src.app.config.config import *
from src.app.utils.utils import Utils
from src.app.config.enumeration import Role, Status


@dataclass
class IssueBookHandler:
    issue_book_service:IssueBookService
    logger = Logger()
    @classmethod
    def create(cls, issue_book_service):
        return cls(issue_book_service)

    @Utils.user
    @api_logger(logger)
    def issue_book_by_user(self):
        try:
            user_id = g.get('user_id')
            if not user_id:
                self.logger.error(INVALID_TOKEN)
                return Response.response(INVALID_TOKEN,Status.FAIL.value,INVALID_CREDENTIALS),401

            request_body = request.get_json()
            try:
                data = IssueBookDTO(**request_body)
            except ValidationError as e:
                self.logger.error(f"Validation Error: {e.json()}")
                return Response.response(INVALID_REQUEST_BODY,Status.FAIL.value,INVALID_REQUEST_BODY_FORMAT),422

            book_id = data.book_id
            return_date = data.return_date
            borrow_date = datetime.now().date()

            # Process the request
            issue_book = IssuedBooks(
                user_id=user_id,
                return_date=return_date,
                borrow_date=borrow_date,
                book_id=book_id
            )
            self.issue_book_service.issue_book(issue_book, book_id)

            self.logger.info(BOOK_ISSUE_SUCCESSFULLY)
            return Response.response(BOOK_ISSUE_SUCCESSFULLY,Status.SUCCESS.value),200
        except Exception as e:
            self.logger.error(str(e))
            return Response.response(SOMETHING_WENT_WRONG, Status.FAIL.value, UNEXPECTED_ERROR), 500

    @Utils.user
    @api_logger(logger)
    def return_book_by_user(self,book_id):
        try:
            user_id = g.get('user_id')
            if not user_id:
                self.logger.error(INVALID_TOKEN)
                return Response.response(INVALID_TOKEN, Status.FAIL.value, INVALID_CREDENTIALS), 401

            self.issue_book_service.return_issue_book(user_id, book_id)
            self.logger.info(RETURN_SUCCESSFULLY)
            return Response.response(RETURN_SUCCESSFULLY, Status.SUCCESS.value),200
        except Exception as e:
            self.logger.error(str(e))
            return Response.response(str(e),Status.FAIL.value,DB_ERROR),500


    @api_logger(logger)
    def get_issued_books(self):
        role = g.get('role')
        if role == Role.USER.value:
            try:
                user_id = g.get('user_id')
                if not user_id:
                    self.logger.error(INVALID_TOKEN)
                    return Response.response(INVALID_TOKEN, Status.FAIL.value, INVALID_CREDENTIALS), 401

                issued_books = self.issue_book_service.get_issue_book_by_user_id(user_id)
                self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                return Response.response(
                    ISSUE_BOOK_FETCH_SUCCESSFULLY,
                    Status.SUCCESS.value,
                    data=[issued_book.__dict__ for issued_book in issued_books] if issued_books else []
                ),200

            except Exception as e:
                self.logger.error(str(e))
                return Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR), 500

        else:
            user_id = request.args.get('user_id')
            if user_id:
                try:
                    issued_books = self.issue_book_service.get_issue_book_by_user_id(user_id)
                    self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                    return Response.response(
                        ISSUE_BOOK_FETCH_SUCCESSFULLY,
                        Status.SUCCESS.value,
                        data=[issued_book.__dict__ for issued_book in issued_books] if issued_books else []
                    ), 200
                except Exception as e:
                    self.logger.error(str(e))
                    return Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR), 500

            else:
                try:
                    issued_books = self.issue_book_service.get_all_issued_books()
                    self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                    return Response.response(
                        ISSUE_BOOK_FETCH_SUCCESSFULLY,
                        Status.SUCCESS.value,
                        data=[issued_book.__dict__ for issued_book in issued_books] if issued_books else []
                    ), 200
                except Exception as e:
                    self.logger.error(str(e))
                    return Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR), 500