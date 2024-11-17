from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.entities.users import User
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository


_local_storage: list[Chat] = []


@dataclass
class MemoryChatRepository(BaseChatRepository):
    async def add_chat(self, chat: Chat):
        _local_storage.append(chat)

    async def get_chat_by_chat_oid(self, chat_oid: str) -> Chat | None:
        try:
            return next(chat for chat in _local_storage if chat.oid == chat_oid)
        except StopIteration:
            return None

    async def delete_chat_by_chat_oid(self, chat_oid: str):
        for chat in _local_storage:
            if chat.oid == chat_oid:
                _local_storage.remove(chat)
                break

    async def get_chats_by_user_oid(self, user_oid: str) -> list[Chat]:
        chats = []
        for chat in _local_storage:
            for user in chat.users:
                if user.oid == user_oid:
                    chats.append(chat)
                    break
        return chats

    async def add_user_to_chat(self, user: User, chat: Chat):
        if user not in chat.users and len(chat.users) < 2:
            chat.users.add(user)


@dataclass
class MemoryMessageRepository(BaseMessageRepository):
    async def add_message(self, message: Message):
        chat = next(chat for chat in _local_storage if chat.oid == message.chat_oid)
        chat.add_message(message)

    async def get_message_by_message_oid(self, message_oid: str) -> Message:
        for chat in _local_storage:
            for message in chat.messages:
                if message.oid == message_oid:
                    return message

    async def get_messages_by_chat_oid(self, chat_oid) -> list[Message]:
        return [
            message
            for chat in _local_storage
            if chat.oid == chat_oid
            for message in chat.messages
        ]
