class ServiceError(Exception):
    """A business-rule violation with a message that is safe to show the user."""


class RateLimited(ServiceError):
    pass
