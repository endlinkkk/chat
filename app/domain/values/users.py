import re
from dataclasses import dataclass

from domain.exceptions.users import (
    EmptyPhoneException,
    EmptyUsernameException,
    FormatPhoneException,
    PasswordTooShortException,
)
from domain.values.base import BaseValue

import bcrypt


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

    # def get_hash_password(self) -> bytes:
    #     salt = bcrypt.gensalt()
    #     pwd_bytes = self.value.encode()
    #     return bcrypt.hashpw(pwd_bytes, salt)

    # def validate_password(self, password: str) -> bool:
    #     hash_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    #     return bcrypt.checkpw(password=self.value.encode(), hashed_password=hash_pwd)
