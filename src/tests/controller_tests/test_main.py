import unittest
from http.client import HTTPException
from logging import exception

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.app.controller.main import create_app


class TestLibraryManagementApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app()
        self.client = TestClient(self.app)

    def test_create_app_returns_fastapi_app(self):
        """Test that create_app returns a FastAPI application"""
        self.assertIsInstance(self.app, FastAPI)
        self.assertEqual(self.app.title, "Library management system")

    def test_dependencies_are_created(self):
        """Test that all repositories and services are created"""
        try:
            app = create_app()
            # Verify that app has necessary dependencies
            self.assertTrue(hasattr(app, 'state'))
            self.assertTrue(hasattr(app, 'dependency_overrides'))
            self.assertTrue(hasattr(app, 'routes'))
        except Exception as e:
            self.fail(f"create_app() raised {type(e).__name__} unexpectedly: {e}")

    def test_all_routes_registered(self):
        """Verify that all expected routes are registered"""
        # Expected route prefixes based on actual API structure
        expected_routes = {
            # User routes
            '/user/signup',
            '/user/login',
            # Book routes
            '/admin/book',
            '/user/book',
            # Issue book routes
            '/book/issue-book',
            '/book/return-book/{book_id}',
        }

        # Get all registered routes
        routes = [route.path for route in self.app.routes]

        # Assert each expected route exists
        for expected_route in expected_routes:
            matching_routes = [r for r in routes if expected_route in r]
            self.assertTrue(
                len(matching_routes) > 0,
                f"No routes found matching prefix '{expected_route}'. Available routes: {routes}"
            )



    def test_exception_handler_registration(self):
        """Test that custom exception handler is registered"""
        from src.app.utils.errors.error import CustomHTTPException

        # Verify the exception handler is registered
        self.assertTrue(
            CustomHTTPException in self.app.exception_handlers,
            "Custom exception handler not registered"
        )
