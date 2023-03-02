class CapsolverError(Exception):
    def __init__(self, message=None, http_body=None, http_status=None, json_body=None, headers=None):
        super(CapsolverError, self).__init__(message)

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}

    def __str__(self):
        return f"{type(self).__name__}: {self._message}" or "<empty message>"


class InvalidRequestError(CapsolverError):
    pass

class IncompleteJobError(CapsolverError):
    pass


class RateLimitError(CapsolverError):
    pass


class AuthenticationError(CapsolverError):
    pass


class InsufficientCreditError(CapsolverError):
    pass


class UnknownError(CapsolverError):
    pass


class Timeout(CapsolverError):
    pass


class APIError(CapsolverError):
    pass


class ServiceUnavailableError(CapsolverError):
    pass
