from faker import Faker
from domain.entities.messages import Chat, Message
from domain.entities.users import User
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.users.base import BaseUserRepository
from logic.commands.messages import AddUserToChatCommand, CreateChatCommand, CreateMessageCommand, GetUserChatMessagesCommand, GetUsersCommand
from logic.mediator import Mediator

import pytest

@pytest.mark.asyncio
async def test_create_chat_command_succes(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
    user: User
):
    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=faker.text(max_nb_chars=10), user=user)
    )
    chat_from_repo = await chat_repository.get_chat_by_chat_oid(chat_oid=chat.oid)
    assert chat.oid == chat_from_repo.oid

    

@pytest.mark.asyncio
async def test_create_message_command_success(
    message_repository: BaseMessageRepository,
    mediator: Mediator,
    faker: Faker,
    user: User,
):
    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=faker.text(max_nb_chars=10), user=user)
    )
    message, *_ = await mediator.handle_command(
        CreateMessageCommand(text='hello', chat_oid=chat.oid, user=user)
    )
    message_from_repo: Message = await message_repository.get_message_by_message_oid(message.oid)

    assert message_from_repo.oid == message.oid
    assert message_from_repo.sender_oid == user.oid
    assert message_from_repo.text.value == 'hello'


@pytest.mark.asyncio
async def test_get_chat_messages(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
    user: User
):
    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=faker.text(max_nb_chars=10), user=user)
    )
    await mediator.handle_command(
        CreateMessageCommand(text='message1', chat_oid=chat.oid, user=user)
    )
    await mediator.handle_command(
        CreateMessageCommand(text='message2', chat_oid=chat.oid, user=user)
    )
    messages, *_ = await mediator.handle_command(GetUserChatMessagesCommand(user=user, chat_oid=chat.oid))

    assert len(messages) == 2


@pytest.mark.asyncio
async def test_add_user_to_chat_command_success(
    chat_repository: BaseChatRepository,
    user_repository: BaseUserRepository,
    mediator: Mediator,
    faker: Faker,
    user: User,
    user2: User
):
    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=faker.text(max_nb_chars=10), user=user)
    )

    await user_repository.add_user(user2)

    await mediator.handle_command(
        AddUserToChatCommand(user_oid=user2.oid, chat_oid=chat.oid, user=user)
    )

    chat_from_repo = await chat_repository.get_chat_by_chat_oid(chat_oid=chat.oid)
    assert user2.oid in [member.oid for member in chat_from_repo.users]


@pytest.mark.asyncio
async def test_get_users_command_success(
    user_repository: BaseUserRepository,
    mediator: Mediator,
    faker: Faker,
    user: User,
    users: list[User]
):

    for f_user in users:
        await user_repository.add_user(f_user)

    users_from_repo, *_ = await mediator.handle_command(GetUsersCommand(user=user))

    assert len(users) == len(users_from_repo) 

