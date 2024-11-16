from dataclasses import dataclass

from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import (
    AccessDeniedException,
    InvalidTokenException,
    UserNotConfirmedException,
    UserNotFoundException,
)
from logic.services.auth import AuthService


@dataclass(frozen=True)
class AccessCheckModeratorCommand(BaseCommand):
    access_token: str


@dataclass(frozen=True)
class AccessCheckModeratorCommandHandler(
    BaseCommandHandler[AccessCheckModeratorCommand, User]
):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: AccessCheckModeratorCommand) -> User:
        payload = await self.auth_service.decode_jwt(
            token=command.access_token,
        )

        if payload is None:
            raise InvalidTokenException()

        user = await self.user_repository.get_user_by_user_oid(payload.get("sub"))

        if not user:
            raise UserNotFoundException()

        if user.is_moderator is False:
            raise AccessDeniedException()

        return user


@dataclass(frozen=True)
class AccessCheckUserCommand(BaseCommand):
    access_token: str


@dataclass(frozen=True)
class AccessCheckUserCommandHandler(BaseCommandHandler[AccessCheckUserCommand, User]):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: AccessCheckUserCommand) -> User:
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

        return user
