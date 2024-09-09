# exceptions.py

class DocumentNotFoundError(Exception):
    """Exception raised when a document is not found in MongoDB."""
    pass

class InvalidDataError(Exception):
    """Exception raised when provided data is invalid."""
    pass

class PermissionDeniedError(Exception):
    """Exception raised when a user does not have permission to perform an action."""
    pass