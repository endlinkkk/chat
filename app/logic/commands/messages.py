from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.entities.users import User
from domain.values.messages import Text, Title
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import (
    InvalidTokenException,
    UserNotConfirmedException,
    UserNotFoundException,
)
from logic.services.auth import AuthService


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str
    access_token: str


@dataclass(frozen=True)
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, Chat]):
    user_repository: BaseUserRepository
    chat_repository: BaseChatRepository
    auth_service: AuthService

    async def handle(self, command: CreateChatCommand) -> Chat:
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()

        title = Title(value=command.title)
        chat = Chat.create_chat(title=title)
        chat.add_user(user)

        await self.chat_repository.add_chat(chat)

        return chat


@dataclass(frozen=True)
class GetUserChatsCommand(BaseCommand):
    access_token: str


@dataclass(frozen=True)
class GetUserChatsCommandHandler(BaseCommandHandler[GetUserChatsCommand, list[Chat]]):
    user_repository: BaseUserRepository
    chat_repository: BaseChatRepository
    auth_service: AuthService

    async def handle(self, command: CreateChatCommand) -> list[Chat]:
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()

        chats = await self.chat_repository.get_chats_by_user_oid(user.oid)

        return chats


@dataclass(frozen=True)
class GetUserChatMessagesCommand(BaseCommand):
    access_token: str
    chat_oid: str


@dataclass(frozen=True)
class GetUserChatMessagesCommandHandler(
    BaseCommandHandler[GetUserChatMessagesCommand, list[Message]]
):
    user_repository: BaseUserRepository
    message_repository: BaseMessageRepository
    auth_service: AuthService

    async def handle(self, command) -> list[Message]:
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()

        messages = await self.message_repository.get_messages_by_chat_oid(
            command.chat_oid
        )
        return messages


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str
    access_token: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    user_repository: BaseUserRepository
    message_repository: BaseMessageRepository
    auth_service: AuthService

    async def handle(self, command: CreateMessageCommand) -> Chat:
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()

        text = Text(value=command.text)

        message = Message(text=text, sender_oid=user.oid, chat_oid=command.chat_oid)

        await self.message_repository.add_message(message)

        return message


@dataclass(frozen=True)
class AddUserToChatCommand(BaseCommand):
    user_oid: str
    chat_oid: str
    access_token: str


@dataclass(frozen=True)
class AddUserToChatCommandHandler(BaseCommandHandler[AddUserToChatCommand, None]):
    user_repository: BaseUserRepository
    chat_repository: BaseChatRepository
    auth_service: AuthService

    async def handle(self, command: AddUserToChatCommand):
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()
        
        invited = await self.user_repository.get_user_by_user_oid(user_oid=command.user_oid)

        if not invited:
            raise UserNotFoundException()

        chat = await self.chat_repository.get_chat_by_chat_oid(chat_oid=command.chat_oid)

        await self.chat_repository.add_user_to_chat(user=invited, chat=chat)


@dataclass(frozen=True)
class GetUsersCommand(BaseCommand):
    access_token: str


@dataclass(frozen=True)
class GetUsersCommandHandler(BaseCommandHandler[GetUsersCommand, list[User]]):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: GetUsersCommand) -> list[User]:
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()
        
        users = await self.user_repository.get_users(limit=10)

        return users
