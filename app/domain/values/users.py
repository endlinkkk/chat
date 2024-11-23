import re
from dataclasses import dataclass

from domain.exceptions.users import (
    EmptyPhoneException,
    EmptyUsernameException,
    FormatPhoneException,
    PasswordTooShortException,
)
from domain.values.base import BaseValue


@dataclass(frozen=True)
class Username(BaseValue):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyUsernameException()


@dataclass(frozen=True)
class Phone(BaseValue):
    value: str

    def validate(self):
        pattern = r"^\+7\d{10}$"

        if not self.value:
            raise EmptyPhoneException()

        # if not re.match(pattern, self.value):
        #     raise FormatPhoneException(self.value)


@dataclass(frozen=True)
class Password(BaseValue):
    value: bytes

    def validate(self):
        if len(self.value) < 10:
            raise PasswordTooShortException()
