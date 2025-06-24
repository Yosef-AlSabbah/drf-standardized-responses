"""
Standardized response structures for Django REST Framework.

This module provides classes and utilities to create consistent API responses
across a Django REST Framework application.
"""
from typing import Any, Dict, Optional, Union
from rest_framework.response import Response


class StandardResponse:
    """
    A utility class for creating standardized API responses.

    This class provides static methods to generate consistently structured
    response dictionaries for both successful and error responses.

    Attributes:
        None (this is a utility class with static methods)
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation successful",
        meta: Optional[Dict[str, Any]] = None,
        status_code: int = 200,
    ) -> Response:
        """
        Create a standardized success response.

        Args:
            data: The main response data to return.
            message: A human-readable success message.
            meta: Additional metadata to include in the response.
            status_code: The HTTP status code for the response.

        Returns:
            Response: A DRF Response object with standardized structure.
        """
        response_data = {
            "success": True,
            "message": message,
            "data": data if data is not None else {},
        }

        if meta:
            response_data["meta"] = meta

        return Response(response_data, status=status_code)

    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: Optional[Union[Dict, list]] = None,
        status_code: int = 400,
    ) -> Response:
        """
        Create a standardized error response.

        Args:
            message: A human-readable error message.
            errors: Detailed error information (can be a dict or list).
            status_code: The HTTP status code for the response.

        Returns:
            Response: A DRF Response object with standardized structure.
        """
        response_data = {
            "success": False,
            "message": message,
            "data": {},
        }

        if errors:
            response_data["errors"] = errors

        return Response(response_data, status=status_code)
