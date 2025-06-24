"""
Tests for the standardized exception handler.

This module tests the exception handler's functionality in
consistently formatting API error responses.
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, NotFound
from rest_framework.test import APIRequestFactory

from drf_standardized_responses.exceptions import standardized_exception_handler


class TestExceptionHandler:
    """Tests for the standardized_exception_handler function."""

    def setup_method(self):
        """Set up the test environment."""
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/api/test/')
        self.context = {'request': self.request}

    def test_validation_error_handling(self):
        """Test that validation errors are properly formatted."""
        # Create a validation error with field-specific errors
        errors = {
            'name': ['This field is required'],
            'email': ['Enter a valid email address']
        }
        exception = ValidationError(errors)

        # Process the exception with the handler
        response = standardized_exception_handler(exception, self.context)

        # Check that the response has the expected structure
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False
        assert response.data['message'] == 'Validation failed'
        assert 'errors' in response.data
        assert response.data['errors'] == errors

    def test_not_found_error_handling(self):
        """Test that 404 errors are properly formatted."""
        # Create a NotFound exception
        exception = NotFound('Resource not found')

        # Process the exception with the handler
        response = standardized_exception_handler(exception, self.context)

        # Check that the response has the expected structure
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['success'] is False
        assert response.data['message'] == 'Resource not found'
        assert 'errors' not in response.data

    def test_http_404_handling(self):
        """Test that Django's Http404 exceptions are properly formatted."""
        # Create a Django Http404 exception
        exception = Http404('Page not found')

        # Process the exception with the handler
        response = standardized_exception_handler(exception, self.context)

        # Check that the response has the expected structure
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['success'] is False
        assert 'Page not found' in response.data['message']
        assert 'errors' not in response.data

    def test_generic_api_exception_handling(self):
        """Test that generic API exceptions are properly formatted."""
        # Create a custom API exception
        class CustomException(APIException):
            status_code = status.HTTP_403_FORBIDDEN
            default_detail = 'You do not have permission'

        exception = CustomException()

        # Process the exception with the handler
        response = standardized_exception_handler(exception, self.context)

        # Check that the response has the expected structure
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['success'] is False
        assert response.data['message'] == 'You do not have permission'
        assert 'errors' not in response.data

    def test_exception_with_custom_detail(self):
        """Test handling exceptions with custom details."""
        # Create an exception with a custom detail message
        exception = APIException('Custom error message')

        # Process the exception with the handler
        response = standardized_exception_handler(exception, self.context)

        # Check that the response has the expected structure
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['success'] is False
        assert response.data['message'] == 'Custom error message'

    def test_unhandled_exception(self, monkeypatch):
        """Test that unhandled exceptions return a generic 500 error."""
        # Mock the default exception handler to return None
        def mock_exception_handler(exc, context):
            return None

        # Use monkeypatch instead of mocker
        import drf_standardized_responses.exceptions
        monkeypatch.setattr(drf_standardized_responses.exceptions, 'exception_handler', mock_exception_handler)

        # Create a standard Python exception
        exception = ValueError('Something went wrong')

        # Process the exception with the handler
        response = standardized_exception_handler(exception, self.context)

        # Check that the response has the expected structure
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['success'] is False
        assert response.data['message'] == 'Internal server error'
        assert 'errors' not in response.data
