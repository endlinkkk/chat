from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    @property
    def message(self):
        return "User not found"


@dataclass(eq=False)
class CodeNotVerifiedException(LogicException):
    @property
    def message(self):
        return "Code not verified"


@dataclass(eq=False)
class UserNotConfirmedException(LogicException):
    @property
    def message(self):
        return "User not confirmed"


@dataclass(eq=False)
class ThisNumberIsAlreadyRegisteredException(LogicException):
    @property
    def message(self):
        return "A user with this number is already registered"


@dataclass(eq=False)
class PasswordNotVerifiedException(LogicException):
    @property
    def message(self):
        return "Password not verified"


@dataclass(eq=False)
class PhoneNotVerifiedException(LogicException):
    @property
    def message(self):
        return "Phone not verified"


@dataclass(eq=False)
class InvalidTokenException(LogicException):
    @property
    def message(self):
        return "Invalid token"


@dataclass(eq=False)
class AccessDeniedException(LogicException):
    @property
    def message(self):
        return "This profile does not have the required permissions"