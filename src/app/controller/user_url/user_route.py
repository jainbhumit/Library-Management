from flask import Blueprint, request, jsonify
from src.app.controller.user_url.user_handler import UserHandler
from src.app.middleware.middleware import auth_middleware
from src.app.services.user_service import UserService

def create_user_routes(user_service: UserService) -> Blueprint:
    user_routes_blueprint = Blueprint('user_routes', __name__)
    user_routes_blueprint.before_request(auth_middleware)
    user_handler = UserHandler.create(user_service)

    user_routes_blueprint.add_url_rule(
        '/login',
        'login',
        user_handler.login,
        methods=['POST']
    )

    user_routes_blueprint.add_url_rule(
        '/signup',
        'signup',
        user_handler.signup,
        methods=['POST']
    )

    return user_routes_blueprint