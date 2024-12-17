from dataclasses import dataclass
from flask import request,g,jsonify
from pydantic import ValidationError

from src.app.config.enumeration import Status
from src.app.config.messages import *
from src.app.config.custome_error_code import *
from src.app.dto.book import CreateBookDTO, UpdateBookDTO
from src.app.model.responses import Response
from src.app.services.book_service import BookService
from src.app.model.books import Books
from src.app.config.config import *
from src.app.utils.errors.error import *
from src.app.utils.logger.logger import Logger
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.utils import Utils

@dataclass
class BookHandler:
    book_service: BookService
    logger = Logger()
    @classmethod
    def create(cls,book_service: BookService):
        return cls(book_service)

    @Utils.admin
    @api_logger(logger)
    def create_book(self):
        try:
            request_body = request.get_json()
            data = CreateBookDTO(**request_body)

            title = data.title
            author = data.author

            book = Books(title=title, author=author)
            self.book_service.add_book(book)
            self.logger.info(BOOK_ADD_SUCCESSFULLY)
            return Response.response(BOOK_ADD_SUCCESSFULLY,Status.SUCCESS.value),200

        except ValidationError as e:
            self.logger.error(f"Validation error: {e.json()}")
            return Response.response(INVALID_REQUEST_BODY,Status.FAIL.value,INVALID_REQUEST_BODY_FORMAT),422

        except Exception as e:
            self.logger.error(str(e))
            return Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR), 500

    @Utils.admin
    @api_logger(logger)
    def update_book(self):
        try:
            request_body = request.get_json()
            data = UpdateBookDTO(**request_body)

            book_id = data.book_id
            title = data.title
            author = data.author

            updated_book = Books(id=book_id, title=title, author=author)
            self.book_service.update_book_by_id(updated_book, book_id)
            self.logger.info(BOOK_UPDATE_SUCCESSFULLY)
            return Response.response(BOOK_UPDATE_SUCCESSFULLY, Status.SUCCESS.value), 200


        except ValidationError as e:
            self.logger.error(f"Validation error: {e.json()}")
            return Response.response(INVALID_REQUEST_BODY, Status.FAIL.value, INVALID_REQUEST_BODY_FORMAT), 422


        except Exception as e:
            self.logger.error(str(e))
            return Response.response(str(e),Status.FAIL.value,UNEXPECTED_ERROR), 500


    @Utils.admin
    @api_logger(logger)
    def remove_book(self,book_id):
        try:
            self.book_service.remove_book_by_id(book_id)
            self.logger.info(BOOK_DELETE_SUCCESSFULLY)
            return Response.response(BOOK_DELETE_SUCCESSFULLY, Status.SUCCESS.value), 200
        except Exception as e:
            self.logger.error(str(e))
            return Response.response(str(e), Status.FAIL.value, DB_ERROR), 500

    @Utils.admin
    @api_logger(logger)
    def delete_book(self,book_id):
        try:
            self.book_service.remove_all_book_by_id(book_id)
            self.logger.info(BOOK_DELETE_SUCCESSFULLY)
            return Response.response(BOOK_DELETE_SUCCESSFULLY, Status.SUCCESS.value), 200

        except Exception as e:
            self.logger.error(str(e))
            return Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR), 500

    @api_logger(logger)
    def get_all_books(self):
        title = request.args.get('title')
        if title is None:
            try:
                books = self.book_service.get_all_books()
                self.logger.info(BOOK_FETCH_SUCCESSFULLY)
                return Response.response(BOOK_FETCH_SUCCESSFULLY, Status.SUCCESS.value,data=[book.__dict__ for book in books] if books else []), 200

            except Exception as e:
                self.logger.error(str(e))
                return Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR), 500

        else:
            try:
                book = self.book_service.get_book_by_title(title)
                self.logger.info(BOOK_FETCH_SUCCESSFULLY)
                return Response.response(BOOK_FETCH_SUCCESSFULLY, Status.SUCCESS.value,data=book.__dict__ if book else {}), 200

            except Exception as e:
                self.logger.error(str(e))
                return Response.response(str(e), Status.FAIL.value, UNEXPECTED_ERROR), 500

