# drf-standardized-responses

[![PyPI](https://img.shields.io/pypi/v/drf-standardized-responses.svg)](https://pypi.org/project/drf-standardized-responses/)
[![CI/CD](https://github.com/Yosef-AlSabbah/drf-standardized-responses/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Yosef-AlSabbah/drf-standardized-responses/actions/workflows/ci-cd.yml)
[![PyPI Downloads](https://static.pepy.tech/badge/drf-standardized-responses)](https://pepy.tech/projects/drf-standardized-responses)
[![Python Version](https://img.shields.io/pypi/pyversions/drf-standardized-responses.svg)](https://pypi.org/project/drf-standardized-responses/)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)

A Django REST Framework utility for standardized API responses, pagination, and exception handling.

---

## Features

- **Consistent Response Format**: All API responses follow a standardized structure (`success`, `message`, `data`, with optional `meta` and `errors` fields).
- **Custom Renderer**: A `StandardResponseRenderer` that formats all responses consistently, preventing common issues like double-wrapping.
- **Standardized Pagination**: `StandardPagination` class that provides rich metadata, including `count`, `total_pages`, and `current_page`.
- **Custom Exception Handler**: A handler that catches DRF exceptions and formats them into the standard error response structure.
- **Helper Functions**: Utilities to easily create standardized success and error responses.

---

## Standard Response Structure

### Success Response

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {
    "id": 1,
    "name": "Item 1"
  }
}
```

### Success Response with Pagination

```json
{
  "success": true,
  "message": "Operation successful",
  "data": [
    {
      "id": 1,
      "name": "Item 1"
    }
  ],
  "meta": {
    "pagination": {
      "count": 100,
      "next": "http://api.example.org/items?page=2",
      "previous": null,
      "total_pages": 10,
      "current_page": 1,
      "page_size": 10
    }
  }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Validation failed",
  "data": {},
  "errors": {
    "name": ["This field is required"],
    "email": ["Enter a valid email address"]
  }
}
```

---

## Installation

```bash
pip install drf-standardized-responses
```

---

## Quick Start

Add the following to your Django `settings.py`:

```python
REST_FRAMEWORK = {
    # Use the custom exception handler
    'EXCEPTION_HANDLER': 'drf_standardized_responses.exceptions.standardized_exception_handler',

    # Use the custom pagination class
    'DEFAULT_PAGINATION_CLASS': 'drf_standardized_responses.pagination.StandardPagination',

    # Use the custom renderer
    'DEFAULT_RENDERER_CLASSES': [
        'drf_standardized_responses.renderers.StandardResponseRenderer',
        # Add other renderers if needed, like BrowsableAPIRenderer
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

---

## API Reference

### `StandardResponse`

A utility class for creating standardized API responses.

```python
from drf_standardized_responses.responses import StandardResponse

# Create a success response
response = StandardResponse.success(
    data={"key": "value"},
    message="Data retrieved successfully",
    meta={"custom_meta": "value"},
    status_code=200
)

# Create an error response
response = StandardResponse.error(
    message="Validation failed",
    errors={"field": ["This field is required"]},
    status_code=400
)
```

### `StandardResponseRenderer`

This renderer automatically wraps your API responses in the standard structure. It correctly handles both error and success responses.

### `StandardPagination`

A pagination class that integrates with the standardized response format to provide consistent pagination metadata.

### `standardized_exception_handler`

An exception handler that catches DRF exceptions and formats them into standardized error responses.

## Testing

Run the test suite:

```bash
pytest
```

---

## Author

- Yousef M. Y. Al Sabbah <itzyousefalsabbah@gmail.com>
- GitHub: [Yosef-AlSabbah](https://github.com/Yosef-AlSabbah)

---

## Contributing

Contributions are welcome! Please check out the [contributing guidelines](CONTRIBUTING.md) for more details on how to contribute to this project.

---

## License

BSD-3-Clause
