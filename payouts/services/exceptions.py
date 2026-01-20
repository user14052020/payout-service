class ServiceError(Exception):
    """Base class for service layer exceptions."""


class PayoutStatusError(ServiceError):
    """Raised when payout status update violates business rules."""
