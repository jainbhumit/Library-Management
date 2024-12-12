from flask import Blueprint, request, jsonify
from src.app.controller.issue_book_url.issue_book_handler import IssueBookHandler
from src.app.middleware.middleware import auth_middleware
from src.app.services.issue_book_service import IssueBookService

def create_issue_book_route(issue_book_service:IssueBookService) -> Blueprint:
    issue_book_routes_blueprint = Blueprint('issue_book_route', __name__)
    issue_book_routes_blueprint.before_request(auth_middleware)
    issue_book_handler = IssueBookHandler.create(issue_book_service)

    issue_book_routes_blueprint.add_url_rule(
        '/issue-book',
        'issue-book',
        issue_book_handler.issue_book_by_user,
        methods=['POST']
    )

    issue_book_routes_blueprint.add_url_rule(
        '/return-book/<book_id>',
        'return-book',
        issue_book_handler.return_book_by_user,
        methods=['PATCH']
    )

    issue_book_routes_blueprint.add_url_rule(
        '/issue-book',
        'get-issue-book',
        issue_book_handler.get_issued_books,
        methods=['GET']
    )
    return issue_book_routes_blueprint
