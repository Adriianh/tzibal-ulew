"""
Custom exceptions for API client communication.
"""

from __future__ import annotations


class ApiError(Exception):
    """Base class for API-related errors."""


class ApiConnectionError(ApiError):
    """Raised when there is a connection error with the API."""


class ApiResponseError(ApiError):
    """Raised when the API returned an error response."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"API responded with status {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class ApiNotFoundError(ApiResponseError):
    """Raised when the API returns a 404 Not Found error."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(404, message)


class ApiValidationError(ApiResponseError):
    """Raised when the API returns a 422 Unprocessable Entity error."""

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(422, message)


class ApiServerError(ApiResponseError):
    """Raised when the API returns a 500 Internal Server Error."""

    def __init__(self, message: str = "Internal server error") -> None:
        super().__init__(500, message)
