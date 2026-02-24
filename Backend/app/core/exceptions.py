class AppException(Exception):
    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)
        
class AuthException(AppException):
    def __init__(self, message = "Authentication Failed"):
        super().__init__(message, code="AUTH_ERROR")

class PermissionDeniedException(AppException):
    def __init__(self, message="Permission Denied"):
        super().__init__(message, code="PERMISSION_DENIED")

class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, code="NOT_FOUND")


class ConflictException(AppException):
    def __init__(self, message="Conflict occurred"):
        super().__init__(message, code="CONFLICT")


class ValidationException(AppException):
    def __init__(self, message="Invalid input"):
        super().__init__(message, code="VALIDATION_ERROR")