from dataclasses import dataclass

from flask import request, jsonify,g
from datetime import datetime

from src.app.model.issued_books import IssuedBooks
from src.app.utils.errors.error import *
from src.app.services.issue_book_service import IssueBookService
from src.app.utils.logger.api_logger import api_logger
from src.app.utils.logger.logger import Logger
from src.app.config.config import *
from src.app.utils.utils import Utils
from src.app.config.types import Role


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
        request_body = request.get_json()
        try:
            user_id = g.get('user_id')
            if not user_id:
                self.logger.error(INVALID_TOKEN)
                return jsonify({"message": INVALID_TOKEN}), 401

            book_id = request_body['book_id']
            if not book_id:
                self.logger.error(INVALID_REQUEST_BODY)
                return jsonify({"message": INVALID_REQUEST_BODY}), 422

            return_date = request_body['return_date']
            if not return_date:
                self.logger.error(INVALID_REQUEST_BODY)
                return jsonify({"message": INVALID_REQUEST_BODY}), 422
            try:
                datetime.strptime(return_date, '%Y-%m-%d')
            except ValueError:
                self.logger.error(INVALID_DATE_FORMAT)
                return jsonify({"message": INVALID_DATE_FORMAT}), 422


            borrow_date = datetime.now().strftime('%Y-%m-%d')
            issue_book = IssuedBooks(user_id=user_id,return_date=return_date,borrow_date=borrow_date,book_id=book_id)

            self.issue_book_service.issue_book(issue_book,book_id)

            self.logger.info(BOOK_ISSUE_SUCCESSFULLY)
            return jsonify({"message":BOOK_ISSUE_SUCCESSFULLY}), 200
        except Exception as e:
            self.logger.error(str(e))
            return jsonify({"message":str(e)}), 500

    @Utils.user
    @api_logger(logger)
    def return_book_by_user(self,book_id):
        try:
            user_id = g.get('user_id')
            if not user_id:
                self.logger.error(INVALID_TOKEN)
                return jsonify({"message": INVALID_TOKEN}), 401

            self.issue_book_service.return_issue_book(user_id, book_id)
            self.logger.info(RETURN_SUCCESSFULLY)
            return jsonify({"message": RETURN_SUCCESSFULLY}), 200
        except Exception as e:
            self.logger.error(str(e))
            return jsonify({"message": str(e)}), 500

    @api_logger(logger)
    def get_issued_books(self):
        role = g.get('role')
        if role == Role.USER.value:
            try:
                user_id = g.get('user_id')
                if not user_id:
                    self.logger.error(INVALID_TOKEN)
                    return jsonify({"message": INVALID_TOKEN}), 401

                issued_books = self.issue_book_service.get_issue_book_by_user_id(user_id)
                self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                return jsonify({"message":ISSUE_BOOK_FETCH_SUCCESSFULLY,"data":[issued_book.__dict__ for issued_book in issued_books] if issued_books else []}), 200
            except Exception as e:
                self.logger.error(str(e))
                return jsonify({"message": str(e)}), 500
        else:
            user_id = request.args.get('user_id')
            if user_id:
                try:
                    issued_books = self.issue_book_service.get_issue_book_by_user_id(user_id)
                    self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                    return jsonify({"message": ISSUE_BOOK_FETCH_SUCCESSFULLY,"data":[issued_book.__dict__ for issued_book in issued_books] if issued_books else []}), 200
                except Exception as e:
                    self.logger.error(str(e))
                    return jsonify({"message": str(e)}), 500
            else:
                try:
                    issued_books = self.issue_book_service.get_all_issued_books()
                    self.logger.info(ISSUE_BOOK_FETCH_SUCCESSFULLY)
                    return jsonify({"message": ISSUE_BOOK_FETCH_SUCCESSFULLY, "data": [issued_book.__dict__ for issued_book in issued_books] if issued_books else []}), 200
                except Exception as e:
                    self.logger.error(str(e))
                    return jsonify({"message": str(e)}), 500







