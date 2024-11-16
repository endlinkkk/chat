from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import Chat
from domain.entities.users import User


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def add_user(self, user: User): ...

    @abstractmethod
    async def get_user_by_user_oid(self, user_oid: str) -> User: ...

    @abstractmethod
    async def delete_user_by_user_oid(self, user_oid: str): ...

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> User: ...


    @abstractmethod
    async def get_users(self, limit: int) -> list[User]: ...
