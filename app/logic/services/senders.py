from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User


@dataclass
class BaseSenderService(ABC):
    @abstractmethod
    async def send_code(self, user: User, code: str) -> None: ...


@dataclass
class DummySenderService(BaseSenderService):
    async def send_code(self, user: User, code: str) -> None:
        print(f"Code sent: {code=}\nTo user: {user=}")


@dataclass
class PhoneSenderService(BaseSenderService):
    async def send_code(self, user: User, code: str) -> None:
        print(f"Code sent: {code}\nTo user phone: {user.credentials.phone.value}")
