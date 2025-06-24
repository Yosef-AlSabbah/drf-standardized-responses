"""
Integration tests for drf-standardized-responses package.

These tests ensure all components work together correctly when used in a Django REST Framework app.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestIntegration:
    """Integration tests for drf-standardized-responses."""

    def setup_method(self):
        """Set up the test client."""
        self.client = APIClient()

    def test_success_response_formatting(self):
        """Test that successful responses are properly formatted."""
        # Get the response from the mock view
        url = reverse('mock-view')
        response = self.client.get(url)

        # Verify the response status and structure
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'message' in response.json()
        assert response.json()['data'] == {'foo': 'bar'}

    def test_pagination_integration(self):
        """Test that paginated responses are properly formatted."""
        # Get the response from the paginated view
        url = reverse('paginated-view')
        response = self.client.get(url)

        # Verify the response status and structure
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'message' in response.json()
        assert isinstance(response.json()['data'], list)

        # Verify pagination metadata
        assert 'meta' in response.json()
        assert 'pagination' in response.json()['meta']
        pagination = response.json()['meta']['pagination']
        assert 'count' in pagination
        assert 'current_page' in pagination
        assert 'total_pages' in pagination
        assert 'page_size' in pagination
        assert 'next' in pagination
        assert 'previous' in pagination

    def test_validation_error_formatting(self):
        """Test that validation errors are properly formatted."""
        # Get the response from the error view with validation error
        url = reverse('error-view') + '?type=validation'
        response = self.client.get(url)

        # Verify the response status and structure
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Validation failed'
        assert 'errors' in response.json()
        assert 'field1' in response.json()['errors']
        assert 'field2' in response.json()['errors']

    def test_not_found_error_formatting(self):
        """Test that not found errors are properly formatted."""
        # Get the response from the error view with not found error
        url = reverse('error-view') + '?type=not_found'
        response = self.client.get(url)

        # Verify the response status and structure
        assert response.status_code == 404
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Resource not found'

    def test_permission_error_formatting(self):
        """Test that permission errors are properly formatted."""
        # Get the response from the error view with permission error
        url = reverse('error-view') + '?type=permission'
        response = self.client.get(url)

        # Verify the response status and structure
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You do not have permission to perform this action'

    def test_preformatted_response_handling(self):
        """Test that already formatted responses are not double-wrapped."""
        # Get the response from the preformatted view
        url = reverse('preformatted-view')
        response = self.client.get(url)

        # Verify the response is not double-wrapped
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['message'] == 'Pre-formatted response'
        assert response.json()['data'] == {'test': 'value'}

        # There should be no nested data or success fields
        assert 'success' not in response.json()['data']
