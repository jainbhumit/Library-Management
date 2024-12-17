from flask import Flask

from src.app.controller.book.route import create_book_route
from src.app.controller.user.route import create_user_routes
from src.app.controller.issue_book.route import create_issue_book_route
from src.app.repositories.user_repository import UserRepository
from src.app.repositories.issued_book_repository import IssuedBookRepository
from src.app.repositories.books_repository import BooksRepository
from src.app.services.issue_book_service import IssueBookService
from src.app.services.book_service import BookService
from src.app.services.user_service import UserService
from src.app.utils.db.db import DB

def create_app():
    app = Flask(__name__)

    db = DB()

    user_repository = UserRepository(db)
    issue_book_repository = IssuedBookRepository(db)
    book_repository = BooksRepository(db)

    user_service = UserService(user_repository)
    book_service = BookService(book_repository)
    issue_book_service = IssueBookService(issue_book_repository,book_repository)

    app.register_blueprint(
        create_user_routes(user_service),
        url_prefix='/user'
    )

    app.register_blueprint(
        create_issue_book_route(issue_book_service),
        url_prefix='/book'
    )

    app.register_blueprint(
        create_book_route(book_service)

    )
    @app.route('/')
    def index():
        return "Health Good"
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)