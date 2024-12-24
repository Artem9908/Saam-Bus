class DocumentServiceException(Exception):
    """Base exception for document service"""
    pass

class ValidationError(DocumentServiceException):
    """Validation error for document data"""
    pass

class GoogleAPIError(DocumentServiceException):
    """Google API related errors"""
    pass

class TemplateError(DocumentServiceException):
    """Template related errors"""
    pass

class DatabaseError(DocumentServiceException):
    """Database related errors"""
    pass 