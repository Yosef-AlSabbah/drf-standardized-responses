"""
Tests for the StandardPagination class.

This module tests the StandardPagination class functionality for providing
standardized paginated responses.
"""
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory
from rest_framework.request import Request

from drf_standardized_responses.pagination import StandardPagination


class TestStandardPagination:
    """Tests for the StandardPagination class."""

    def setup_method(self):
        """Set up the test environment."""
        self.pagination = StandardPagination()
        self.factory = RequestFactory()

    def test_pagination_attributes(self):
        """Test that pagination attributes are correctly set."""
        assert self.pagination.page_size == 10
        assert self.pagination.page_size_query_param == 'page_size'
        assert self.pagination.max_page_size == 100
        assert self.pagination.page_query_param == 'page'

    def test_get_paginated_response(self):
        """Test that get_paginated_response returns a correctly structured response."""
        # Mock the necessary pagination attributes and methods
        data = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

        # Create a mock request
        request = Request(self.factory.get('/'))
        self.pagination.request = request

        # Mock the pagination page attributes
        self.pagination.page = MagicMock()
        self.pagination.page.paginator.count = 10
        self.pagination.page.number = 1
        self.pagination.page.paginator.num_pages = 5

        # Mock the necessary methods
        self.pagination.get_next_link = MagicMock(return_value="http://testserver/api/items?page=2")
        self.pagination.get_previous_link = MagicMock(return_value=None)
        self.pagination.get_page_size = MagicMock(return_value=10)

        # Get the paginated response
        response = self.pagination.get_paginated_response(data)

        # Check the response structure
        assert response.status_code == 200
        assert response.data["success"] is True
        assert "message" in response.data
        assert response.data["data"] == data

        # Check pagination metadata
        assert "meta" in response.data
        assert "pagination" in response.data["meta"]
        pagination_meta = response.data["meta"]["pagination"]

        assert pagination_meta["count"] == 10
        assert pagination_meta["current_page"] == 1
        assert pagination_meta["total_pages"] == 5
        assert pagination_meta["page_size"] == 10
        assert pagination_meta["next"] == "http://testserver/api/items?page=2"
        assert pagination_meta["previous"] is None

    def test_pagination_with_custom_page_size(self):
        """Test pagination with a custom page size from query parameters."""
        # Create a request with a page_size parameter
        request = Request(self.factory.get('/?page_size=5'))

        # Setup the pagination with the request
        self.pagination.request = request

        # Test the get_page_size method
        page_size = self.pagination.get_page_size(request)
        assert page_size == 5

    def test_pagination_with_invalid_page_size(self):
        """Test pagination with an invalid page size parameter."""
        # Create a request with an invalid page_size parameter
        request = Request(self.factory.get('/?page_size=invalid'))

        # Setup the pagination with the request
        self.pagination.request = request

        # Should fall back to default page size
        page_size = self.pagination.get_page_size(request)
        assert page_size == 10

    def test_pagination_with_excessive_page_size(self):
        """Test pagination with a page size that exceeds the maximum."""
        # Create a request with a page_size parameter that exceeds max_page_size
        request = Request(self.factory.get('/?page_size=200'))

        # Setup the pagination with the request
        self.pagination.request = request

        # Should be capped at max_page_size
        page_size = self.pagination.get_page_size(request)
        assert page_size == 100  # max_page_size value
