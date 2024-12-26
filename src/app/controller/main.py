from fastapi import FastAPI

from src.app.controller.issue_book.route import create_issue_book_route
from src.app.controller.user.route import create_user_routes
from src.app.controller.book.route import create_book_route
from src.app.middleware.middleware import AuthMiddleware
from src.app.repositories.user_repository import UserRepository
from src.app.repositories.issued_book_repository import IssuedBookRepository
from src.app.repositories.books_repository import BooksRepository
from src.app.services.issue_book_service import IssueBookService
from src.app.services.book_service import BookService
from src.app.services.user_service import UserService
from src.app.utils.db.db import DB
from src.app.utils.errors.error import CustomHTTPException, custom_http_exception_handler
from src.app.utils.logger.logger import LoggerMiddleware


def create_app():
    app = FastAPI(title="Library management system")
    app.add_middleware(LoggerMiddleware)
    app.add_middleware(AuthMiddleware)

    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)

    db = DB()

    user_repository = UserRepository(db)
    issue_book_repository = IssuedBookRepository(db)
    book_repository = BooksRepository(db)

    user_service = UserService(user_repository)
    book_service = BookService(book_repository)
    issue_book_service = IssueBookService(issue_book_repository,book_repository)

    app.include_router(create_user_routes(user_service))
    app.include_router(create_issue_book_route(issue_book_service))
    app.include_router(create_book_route(book_service))

    return app

if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=5000)