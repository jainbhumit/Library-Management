from dataclasses import dataclass

from fastapi import Request,HTTPException
from datetime import datetime

from pydantic import ValidationError
from starlette import status

from src.app.config.custome_error_code import *
from src.app.config.messages import *
from src.app.dto.issue_book import IssueBookDTO
from src.app.model.issued_books import IssuedBooks
from src.app.model.responses import Response, CustomErrorResponse
from src.app.utils.context import get_user_from_context
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
    def issue_book_by_user(self,request:Request,request_body:IssueBookDTO):
        try:
            user_ctx = get_user_from_context(request)
            user_id = user_ctx.get('user_id')
            if not user_id:
                self.logger.error(INVALID_TOKEN)
                return CustomErrorResponse.error_response(
                    Response.response(INVALID_TOKEN,Status.FAIL.value,INVALID_CREDENTIALS),
                    500
                )

            borrow_date = datetime.now().date()

            # Process the request
            issue_book = IssuedBooks(
                user_id=user_id,
                return_date=request_body.return_date,
                borrow_date=borrow_date,
                book_id=request_body.book_id
            )
            self.issue_book_service.issue_book(issue_book, request_body.book_id)

            self.logger.info(BOOK_ISSUE_SUCCESSFULLY)
            return Response.response(BOOK_ISSUE_SUCCESSFULLY,Status.SUCCESS.value)
        except NotExistsError as e:
            return CustomErrorResponse.error_response(
                Response.response(str(e), Status.FAIL.value,NOT_EXISTS),
                200
            )
        except InvalidOperationError as e:
            return CustomErrorResponse.error_response(
                Response.response(str(e), Status.FAIL.value, NOT_EXISTS),
                200
            )
        except Exception as e:
            self.logger.error(str(e))
            return CustomErrorResponse.error_response(
                Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR),
                500
            )


    @Utils.user
    @api_logger(logger)
    def return_book_by_user(self,book_id,request:Request):
        try:
            user_ctx = get_user_from_context(request)
            user_id = user_ctx.get('user_id')
            if not user_id:
                self.logger.error(INVALID_TOKEN)
                return CustomErrorResponse.error_response(
                    Response.response(INVALID_TOKEN, Status.FAIL.value, INVALID_CREDENTIALS),
                    500
                )

            self.issue_book_service.return_issue_book(user_id, book_id)
            self.logger.info(RETURN_SUCCESSFULLY)
            return Response.response(RETURN_SUCCESSFULLY, Status.SUCCESS.value)

        except NotExistsError as e:
            return CustomErrorResponse.error_response(
                Response.response(str(e), Status.FAIL.value,NOT_EXISTS),
                200
            )
        except Exception as e:
            self.logger.error(str(e))
            return CustomErrorResponse.error_response(
                Response.response(str(e),Status.FAIL.value,DB_ERROR),
                500
            )


    @api_logger(logger)
    def get_issued_books(self,request:Request):
        user_ctx = get_user_from_context(request)
        print(user_ctx)
        role = user_ctx.get('role')
        if role == Role.USER.value:
            try:
                user_id = user_ctx.get('user_id')
                if not user_id:
                    self.logger.error(INVALID_TOKEN)
                    return CustomErrorResponse.error_response(
                        Response.response(INVALID_TOKEN, Status.FAIL.value, INVALID_CREDENTIALS),
                        500
                    )

                issued_books = self.issue_book_service.get_issue_book_by_user_id(user_id)
                self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                return Response.response(
                    ISSUE_BOOK_FETCH_SUCCESSFULLY,
                    Status.SUCCESS.value,
                    data=[issued_book.__dict__ for issued_book in issued_books] if issued_books else []
                )

            except Exception as e:
                self.logger.error(str(e))
                return CustomErrorResponse.error_response(
                    Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR),
                    500
                )

        else:
            user_id = request.query_params.get('user_id')
            if user_id:
                try:
                    issued_books = self.issue_book_service.get_issue_book_by_user_id(user_id)
                    self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                    return Response.response(
                        ISSUE_BOOK_FETCH_SUCCESSFULLY,
                        Status.SUCCESS.value,
                        data=[issued_book.__dict__ for issued_book in issued_books] if issued_books else []
                    )
                except Exception as e:
                    self.logger.error(str(e))
                    return CustomErrorResponse.error_response(
                        Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR),
                        500
                    )
            else:
                try:
                    issued_books = self.issue_book_service.get_all_issued_books()
                    self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                    return Response.response(
                        ISSUE_BOOK_FETCH_SUCCESSFULLY,
                        Status.SUCCESS.value,
                        data=[issued_book.__dict__ for issued_book in issued_books] if issued_books else []
                    )
                except Exception as e:
                    self.logger.error(str(e))
                    return CustomErrorResponse.error_response(
                        Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR),
                        500
                    )