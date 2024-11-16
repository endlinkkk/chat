from dataclasses import dataclass

from domain.exceptions.messages import (
    EmptyTextException,
    EmptyTitleException,
    TitleTooLongException,
)
from domain.values.base import BaseValue


@dataclass(frozen=True)
class Text(BaseValue):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValue):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTitleException()

        if len(self.value) > 64:
            raise TitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
