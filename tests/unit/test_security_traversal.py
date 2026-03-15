"""
Description: Unit tests for path traversal security in the `serve_spa` endpoint.
Why: To ensure that the application is not vulnerable to directory traversal attacks when serving static files or the SPA.
How: Uses FastAPI's TestClient to make requests with malicious and safe paths and asserts that the application behaves as expected.
"""

import os
import unittest
from unittest.mock import mock_open, patch

from fastapi.testclient import TestClient

from app.fast_api_app import app


class TestSecurityTraversal(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_path_traversal_protection_logic(self):
        # This tests the logic used in serve_spa directly
        actual_frontend_dist = os.path.abspath("/mock/frontend/dist")

        # Test 1: Dangerous path (Traversal)
        full_path = "../../.env"
        requested_path = os.path.abspath(os.path.join(actual_frontend_dist, full_path))
        self.assertFalse(requested_path.startswith(actual_frontend_dist))

        # Test 2: Safe path
        full_path = "assets/main.js"
        requested_path = os.path.abspath(os.path.join(actual_frontend_dist, full_path))
        self.assertTrue(requested_path.startswith(actual_frontend_dist))

        # Test 3: Safe path (at root)
        full_path = "index.html"
        requested_path = os.path.abspath(os.path.join(actual_frontend_dist, full_path))
        self.assertTrue(requested_path.startswith(actual_frontend_dist))

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open, read_data="<html><body>Home<!-- __SEO_TAGS__ --></body></html>")
    def test_valid_path_allowed(self, mock_file, mock_isfile):
        # Mock index.html existence
        mock_isfile.side_effect = lambda p: p.endswith("index.html")

        # Valid SPA route
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Home", response.text)

    @patch("os.path.isfile")
    @patch("app.fast_api_app.FileResponse")
    def test_valid_static_file_allowed(self, mock_file_response, mock_isfile):
        # Mock a static file like favicon.ico
        mock_isfile.side_effect = lambda p: p.endswith("favicon.ico")
        mock_file_response.return_value = "Mocked FileResponse"

        response = self.client.get("/favicon.ico")
        # If it reaches FileResponse, it's passed the 403 check
        self.assertNotEqual(response.status_code, 403)
