from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseUserCache(ABC):
    @abstractmethod
    async def add_code(self, phone: str, code: str): ...

    @abstractmethod
    async def delete_code(self, phone: str): ...

    @abstractmethod
    async def check_code(self, phone: str, code: str) -> bool: ...
