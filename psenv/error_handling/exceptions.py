class PsenvParameterStoreError(Exception):
    pass

class PsenvConfigNotFoundError(Exception):
    pass

class PsenvConfigError(Exception):
    pass

class PsenvInternalError(Exception):
    """Raised for internal errors in psenv."""
    pass
