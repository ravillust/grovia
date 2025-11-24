from typing import Any, Optional


class GroviaException(Exception):
    """Base exception for Grovia"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class AuthenticationError(GroviaException):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
            details=details
        )


class AuthorizationError(GroviaException):
    """Authorization error"""
    
    def __init__(self, message: str = "Access denied", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
            details=details
        )


class NotFoundError(GroviaException):
    """Resource not found error"""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details=details
        )


class ValidationError(GroviaException):
    """Validation error"""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details
        )


class DuplicateError(GroviaException):
    """Duplicate resource error"""
    
    def __init__(self, message: str = "Resource already exists", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=409,
            error_code="DUPLICATE_ERROR",
            details=details
        )


class DetectionError(GroviaException):
    """Detection processing error"""
    
    def __init__(self, message: str = "Detection failed", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DETECTION_ERROR",
            details=details
        )