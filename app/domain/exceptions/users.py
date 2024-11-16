from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class EmptyUsernameException(ApplicationException):
    @property
    def message(self):
        return "Username is not be empty"


@dataclass
class EmptyPhoneException(ApplicationException):
    @property
    def message(self):
        return "Phone is not be empty"


@dataclass
class FormatPhoneException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Phone should be in this format: +79000000000. {self.text}"


@dataclass
class PasswordTooShortException(ApplicationException):
    @property
    def message(self):
        return "Password should be longer"
