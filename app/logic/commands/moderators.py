from dataclasses import dataclass

from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.services.auth import AuthService


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    moderator: User
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(BaseCommandHandler[DeleteUserCommand, None]):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: DeleteUserCommand):
        await self.user_repository.delete_user_by_user_oid(user_oid=command.user_oid)
