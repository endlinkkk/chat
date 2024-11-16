from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Could not find handlers for the command: {self.command_type}"
