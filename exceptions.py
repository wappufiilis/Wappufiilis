class WappufiilisError(Exception):
    """Base exception for all Wappufiilis errors"""
    pass

class DatabaseError(WappufiilisError):
    """Raised when database operations fail"""
    pass

class ValidationError(WappufiilisError):
    """Raised when data validation fails"""
    pass

class ConfigurationError(WappufiilisError):
    """Raised when configuration is invalid or missing"""
    pass 