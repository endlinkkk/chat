from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass


from domain.entities.messages import Chat, Message
from domain.entities.users import User


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def add_chat(self, chat: Chat): ...

    @abstractmethod
    async def get_chat_by_chat_oid(self, chat_oid: str) -> Chat: ...

    @abstractmethod
    async def delete_chat_by_chat_oid(self, chat_oid: str): ...

    @abstractmethod
    async def get_chats_by_user_oid(self, user_oid: str) -> Iterable[Chat]: ...

    @abstractmethod
    async def add_user_to_chat(self, user: User, chat: Chat): ...


@dataclass
class BaseMessageRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message): ...

    @abstractmethod
    async def get_messages_by_chat_oid(self, chat_oid: str) -> Iterable[Message]: ...

    @abstractmethod
    async def get_message_by_message_oid(self, message_oid: str) -> Message: ...
