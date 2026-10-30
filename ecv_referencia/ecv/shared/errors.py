"""Errors raised by the modules for conditions the user can fix (shown as messages by the CLI and the web app)."""


class EcvError(Exception):
    """A request that cannot be carried out as asked (missing domain, step not yet allowed, invalid operation, ...)."""


class DomainError(EcvError):
    pass


class StepError(EcvError):
    pass


class AmendmentError(EcvError):
    pass


class RequestError(EcvError):
    pass
