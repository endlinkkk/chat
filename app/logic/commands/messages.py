from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.entities.users import User
from domain.values.messages import Text, Title
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import (
    UserNotFoundException,
)


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str
    user: User


@dataclass(frozen=True)
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, Chat]):
    user_repository: BaseUserRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        user = command.user

        title = Title(value=command.title)
        chat = Chat.create_chat(title=title)
        chat.add_user(user)

        await self.chat_repository.add_chat(chat)

        return chat


@dataclass(frozen=True)
class GetUserChatsCommand(BaseCommand):
    user: User


@dataclass(frozen=True)
class GetUserChatsCommandHandler(BaseCommandHandler[GetUserChatsCommand, list[Chat]]):
    user_repository: BaseUserRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> list[Chat]:
        user = command.user

        chats = await self.chat_repository.get_chats_by_user_oid(user.oid)

        return chats


@dataclass(frozen=True)
class GetUserChatMessagesCommand(BaseCommand):
    user: User
    chat_oid: str


@dataclass(frozen=True)
class GetUserChatMessagesCommandHandler(
    BaseCommandHandler[GetUserChatMessagesCommand, list[Message]]
):
    user_repository: BaseUserRepository
    message_repository: BaseMessageRepository

    async def handle(self, command) -> list[Message]:
        messages = await self.message_repository.get_messages_by_chat_oid(
            command.chat_oid
        )
        return messages


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str
    user: User


@dataclass(frozen=True)
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    user_repository: BaseUserRepository
    message_repository: BaseMessageRepository

    async def handle(self, command: CreateMessageCommand) -> Chat:
        user = command.user

        text = Text(value=command.text)

        message = Message(text=text, sender_oid=user.oid, chat_oid=command.chat_oid)

        await self.message_repository.add_message(message)

        return message


@dataclass(frozen=True)
class AddUserToChatCommand(BaseCommand):
    user_oid: str
    chat_oid: str
    user: User


@dataclass(frozen=True)
class AddUserToChatCommandHandler(BaseCommandHandler[AddUserToChatCommand, None]):
    user_repository: BaseUserRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: AddUserToChatCommand):
        invited = await self.user_repository.get_user_by_user_oid(
            user_oid=command.user_oid
        )

        if not invited:
            raise UserNotFoundException()

        chat = await self.chat_repository.get_chat_by_chat_oid(
            chat_oid=command.chat_oid
        )

        await self.chat_repository.add_user_to_chat(user=invited, chat=chat)


@dataclass(frozen=True)
class GetUsersCommand(BaseCommand):
    user: User


@dataclass(frozen=True)
class GetUsersCommandHandler(BaseCommandHandler[GetUsersCommand, list[User]]):
    user_repository: BaseUserRepository

    async def handle(self, command: GetUsersCommand) -> list[User]:
        users = await self.user_repository.get_users(limit=10)

        return users
