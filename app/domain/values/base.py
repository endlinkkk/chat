from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

VT = TypeVar("VT", bound=Any)


@dataclass(frozen=True)
class BaseValue(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self): ...
