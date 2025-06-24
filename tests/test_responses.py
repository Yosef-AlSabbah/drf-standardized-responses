"""
Tests for the StandardResponse class.

This module tests the functionality of the StandardResponse class in providing
standardized API responses.
"""
from rest_framework import status

from drf_standardized_responses.responses import StandardResponse


class TestStandardResponse:
    """Tests for the StandardResponse class."""

    def test_success_response_default(self):
        """Test that success method returns a correctly structured response with defaults."""
        response = StandardResponse.success()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Operation successful"
        assert response.data["data"] == {}
        assert "meta" not in response.data

    def test_success_response_with_data(self):
        """Test that success method includes provided data."""
        data = {"key": "value"}
        response = StandardResponse.success(data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Operation successful"
        assert response.data["data"] == data

    def test_success_response_with_custom_message(self):
        """Test that success method uses custom message."""
        message = "Custom success message"
        response = StandardResponse.success(message=message)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == message

    def test_success_response_with_meta(self):
        """Test that success method includes metadata when provided."""
        meta = {"pagination": {"total": 10, "page": 1}}
        response = StandardResponse.success(meta=meta)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["meta"] == meta

    def test_success_response_with_custom_status(self):
        """Test that success method uses custom HTTP status code."""
        response = StandardResponse.success(status_code=status.HTTP_201_CREATED)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True

    def test_error_response_default(self):
        """Test that error method returns a correctly structured response with defaults."""
        response = StandardResponse.error()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "An error occurred"
        assert response.data["data"] == {}
        assert "errors" not in response.data

    def test_error_response_with_custom_message(self):
        """Test that error method uses custom message."""
        message = "Custom error message"
        response = StandardResponse.error(message=message)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == message

    def test_error_response_with_errors(self):
        """Test that error method includes errors when provided."""
        errors = {"field": ["This field is required"]}
        response = StandardResponse.error(errors=errors)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["errors"] == errors

    def test_error_response_with_custom_status(self):
        """Test that error method uses custom HTTP status code."""
        response = StandardResponse.error(status_code=status.HTTP_404_NOT_FOUND)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["success"] is False

    def test_error_response_with_list_errors(self):
        """Test that error method can handle list-type errors."""
        errors = ["Error 1", "Error 2"]
        response = StandardResponse.error(errors=errors)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["errors"] == errors
