from dataclasses import dataclass
from flask import request,g,jsonify

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
    @api_logger
    def create_book(self):
        request_body = request.get_json()
        try:
            title = request_body['title']
            if not title:
                self.logger.error(INVALID_REQUEST_BODY)
                raise InvalidRequestBody(INVALID_REQUEST_BODY)
            author = request_body['author']
            if not author:
                self.logger.error(INVALID_REQUEST_BODY)
                raise InvalidRequestBody(INVALID_REQUEST_BODY)

            book = Books(title=title, author=author)
            self.book_service.add_book(book)
            self.logger.info(BOOK_ADD_SUCCESSFULLY)
            return jsonify({"message":BOOK_ADD_SUCCESSFULLY}), 200

        except Exception as e:
            self.logger.error(str(e))
            return jsonify({"message":str(e)}), 500

    @Utils.admin
    @api_logger
    def update_book(self):
        request_body = request.get_json()
        try:
            book_id = request_body['book_id']
            if not book_id:
                self.logger.error(INVALID_REQUEST_BODY)
                raise InvalidRequestBody(INVALID_REQUEST_BODY)
            title = request_body['title']
            if not title:
                self.logger.error(INVALID_REQUEST_BODY)
                raise InvalidRequestBody(INVALID_REQUEST_BODY)
            author = request_body['author']
            if not author:
                self.logger.error(INVALID_REQUEST_BODY)
                raise InvalidRequestBody(INVALID_REQUEST_BODY)

            updated_book = Books(id=book_id, title=title, author=author)
            self.book_service.update_book_by_id(updated_book, book_id)
            self.logger.info(BOOK_UPDATE_SUCCESSFULLY)
            return jsonify({"message":BOOK_UPDATE_SUCCESSFULLY}) , 200
        except Exception as e:
            self.logger.error(str(e))
            return jsonify({"message":str(e)}), 500

    @Utils.admin
    @api_logger
    def remove_book(self,book_id):
        try:
            self.book_service.remove_book_by_id(book_id)
            self.logger.info(BOOK_DELETE_SUCCESSFULLY)
            return jsonify({"message":BOOK_DELETE_SUCCESSFULLY})
        except Exception as e:
            self.logger.error(str(e))
            return jsonify({"message":str(e)})

    @Utils.admin
    @api_logger
    def delete_book(self,book_id):
        try:
            self.book_service.remove_all_book_by_id(book_id)
            self.logger.info(BOOK_DELETE_SUCCESSFULLY)
            return jsonify({"message":BOOK_DELETE_SUCCESSFULLY})

        except Exception as e:
            self.logger.error(str(e))
            return jsonify({"message":str(e)})


    @Utils.admin
    @api_logger
    def get_all_books(self):
        title = request.args.get('title')
        if not title:
            try:
                books = self.book_service.get_all_books()
                self.logger.info(BOOK_FETCH_SUCCESSFULLY)
                return jsonify({"message":BOOK_FETCH_SUCCESSFULLY,"data":books}), 200
            except Exception as e:
                self.logger.error(str(e))
                return jsonify({"message":str(e)}), 500
        else:
            try:
                book = self.book_service.get_book_by_title(title)
                self.logger.info(BOOK_FETCH_SUCCESSFULLY)
                return jsonify({"message":BOOK_FETCH_SUCCESSFULLY,"data":book}), 200
            except Exception as e:
                self.logger.error(str(e))
                return jsonify({"message":str(e)}), 500
