from flask import Blueprint

from src.app.controller.book.handler import BookHandler
from src.app.middleware.middleware import auth_middleware
from src.app.services.book_service import BookService


def create_book_route(book_service:BookService):
    book_route_blueprint = Blueprint('book_route', __name__)
    book_route_blueprint.before_request(auth_middleware)
    book_handler = BookHandler(book_service)

    book_route_blueprint.add_url_rule(
        '/admin/book',
        "create-book",
        book_handler.create_book,
        methods=['POST']
    )

    book_route_blueprint.add_url_rule(
        '/admin/book',
        "update-book",
        book_handler.update_book,
        methods=['PUT']
    )

    book_route_blueprint.add_url_rule(
        '/admin/book/<book_id>',
        "remove-book",
        book_handler.remove_book,
        methods=['PATCH']
    )

    book_route_blueprint.add_url_rule(
        '/admin/book/<book_id>',
        "delete-book",
        book_handler.delete_book,
        methods=['DELETE']
    )

    book_route_blueprint.add_url_rule(
        '/user/book',
        "get-book",
        book_handler.get_all_books,
        methods=['GET']
    )

    return book_route_blueprint



