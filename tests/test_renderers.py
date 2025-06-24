"""
Tests for the StandardResponseRenderer class.

This module tests the StandardResponseRenderer class functionality for automatically
wrapping API responses in the standardized format.
"""
import json
from unittest.mock import MagicMock

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from drf_standardized_responses.renderers import StandardResponseRenderer


class TestStandardResponseRenderer:
    """Tests for the StandardResponseRenderer class."""

    def setup_method(self):
        """Set up the test environment."""
        self.renderer = StandardResponseRenderer()

    def test_render_already_formatted_response(self):
        """Test that the renderer doesn't rewrap already formatted responses."""
        formatted_data = {
            "success": True,
            "message": "Already formatted",
            "data": {"key": "value"}
        }

        # Create mock renderer context
        response = Response(formatted_data, status=status.HTTP_200_OK)
        renderer_context = {"response": response}

        # Render the response
        rendered = self.renderer.render(formatted_data, None, renderer_context)

        # Check that the rendered output is the same as the input
        result = json.loads(rendered.decode('utf-8'))
        assert result == formatted_data

    def test_render_success_response(self):
        """Test that the renderer properly wraps success responses."""
        data = {"key": "value"}

        # Create mock renderer context
        response = Response(data, status=status.HTTP_200_OK)
        renderer_context = {"response": response}

        # Render the response
        rendered = self.renderer.render(data, None, renderer_context)

        # Check that the response is wrapped in the expected format
        result = json.loads(rendered.decode('utf-8'))
        assert result["success"] is True
        assert "message" in result
        assert result["data"] == data

    def test_render_error_response(self):
        """Test that the renderer properly wraps error responses."""
        data = {"detail": "Not found"}

        # Create mock renderer context
        response = Response(data, status=status.HTTP_404_NOT_FOUND)
        renderer_context = {"response": response}

        # Render the response
        rendered = self.renderer.render(data, None, renderer_context)

        # Check that the response is wrapped in the expected error format
        result = json.loads(rendered.decode('utf-8'))
        assert result["success"] is False
        assert "message" in result
        assert "data" in result

    def test_render_error_response_with_error_detail(self):
        """Test that the renderer properly extracts error details."""
        data = {
            "field1": ["This field is required"],
            "field2": ["This field must be unique"]
        }

        # Create mock renderer context
        response = Response(data, status=status.HTTP_400_BAD_REQUEST)
        renderer_context = {"response": response}

        # Render the response
        rendered = self.renderer.render(data, None, renderer_context)

        # Check that the response has the correct error format
        result = json.loads(rendered.decode('utf-8'))
        assert result["success"] is False
        assert "errors" in result
        assert "field1" in result["errors"]
        assert "field2" in result["errors"]

    def test_render_error_response_with_message(self):
        """Test that the renderer properly extracts error messages."""
        data = {
            "message": "Custom error message",
            "field1": ["This field is required"]
        }

        # Create mock renderer context
        response = Response(data, status=status.HTTP_400_BAD_REQUEST)
        renderer_context = {"response": response}

        # Render the response
        rendered = self.renderer.render(data, None, renderer_context)

        # Check that the response uses the provided message
        result = json.loads(rendered.decode('utf-8'))
        assert result["success"] is False
        assert result["message"] == "Custom error message"
        assert "errors" in result

    def test_render_error_response_with_string_data(self):
        """Test that the renderer handles string error data properly."""
        data = "Something went wrong"

        # Create mock renderer context
        response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        renderer_context = {"response": response}

        # Render the response
        rendered = self.renderer.render(data, None, renderer_context)

        # Check that the response wraps the string properly
        result = json.loads(rendered.decode('utf-8'))
        assert result["success"] is False
        assert result["message"] == "Something went wrong"

    def test_render_no_response_context(self):
        """Test that the renderer handles missing context properly."""
        data = {"key": "value"}

        # Render without a context
        rendered = self.renderer.render(data, None, None)

        # Check that the response is still wrapped as a success
        result = json.loads(rendered.decode('utf-8'))
        assert result["success"] is True
        assert "message" in result
        assert result["data"] == data
