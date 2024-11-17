from faker import Faker
import pytest

from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository
from logic.commands.moderators import DeleteUserCommand
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_delete_user_succes(
    user_repository: BaseUserRepository,
    mediator: Mediator,
    faker: Faker,
    user: User,
    moderator: User,
):
    await user_repository.add_user(user=user)

    await mediator.handle_command(
        DeleteUserCommand(moderator=moderator, user_oid=user.oid)
    )
    user_from_repo = await user_repository.get_user_by_user_oid(user_oid=user.oid)

    assert user_from_repo.is_blocked is True
