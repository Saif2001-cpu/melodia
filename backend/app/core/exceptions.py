"""Custom exception classes and global exception handlers."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException as NotFoundException
from fastapi.responses import JSONResponse


class MelodiaException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class BadRequestError(MelodiaException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class NotFoundError(MelodiaException):
    def __init__(self, resource: str, identifier: Any = None) -> None:
        msg = f"{resource} not found"
        if identifier is not None:
            msg = f"{resource} '{identifier}' not found"
        super().__init__(msg, status.HTTP_404_NOT_FOUND)


class ConflictError(MelodiaException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class UnauthorizedError(MelodiaException):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(MelodiaException):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ValidationError(MelodiaException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class ExternalServiceError(MelodiaException):
    def __init__(self, service: str, message: str) -> None:
        super().__init__(f"{service}: {message}", status.HTTP_502_BAD_GATEWAY)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app."""

    @app.exception_handler(NotFoundException)
    async def http_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
        """Normalize FastAPI/starlette HTTPExceptions into the same envelope
        as MelodiaException so clients always receive ``{error, message}``.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc.detail),
            },
        )

    @app.exception_handler(MelodiaException)
    async def melodia_exception_handler(request: Request, exc: MelodiaException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
                **({"detail": exc.detail} if exc.detail is not None else {}),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred.",
            },
        )
