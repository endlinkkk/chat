from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    @property
    def message(self):
        return "Chat not found"