from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return "Text is not be empty"


@dataclass
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Text too long {self.text[:64]}..."


@dataclass
class EmptyTitleException(ApplicationException):
    @property
    def message(self):
        return "Title is not be empty"
