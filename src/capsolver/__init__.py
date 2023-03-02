import os

from capsolver.capsolver import Capsolver
from capsolver.error import  InvalidRequestError, IncompleteJobError, RateLimitError, AuthenticationError, InsufficientCreditError, UnknownError, Timeout, APIError, ServiceUnavailableError

api_base = os.environ.get("CAPSOLVER_API_BASE", "https://api.capsolver.com")
api_key = os.environ.get("CAPSOLVER_API_KEY")
solve = Capsolver.solve
balance = Capsolver.balance
proxy = None


__all__ = [
    "Capsolver"
    "CAPSOLVERError",
    "InvalidRequestError",
    "IncompleteJobError",
    "RateLimitError",
    "AuthenticationError",
    "InsufficientCreditError",
    "UnknownError",
    "Timeout",
    "APIError",
    "ServiceUnavailableError",

    "api_base",
    "api_key",
    "proxy",
]
