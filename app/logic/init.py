from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from infra.caches.users.base import BaseUserCache
from infra.caches.users.memory import MemoryUserCache
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.messages.memory import (
    MemoryChatRepository,
    MemoryMessageRepository,
)
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from logic.commands.messages import (
    AddUserToChatCommand,
    AddUserToChatCommandHandler,
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
    GetUserChatMessagesCommand,
    GetUserChatMessagesCommandHandler,
    GetUserChatsCommand,
    GetUserChatsCommandHandler,
    GetUsersCommand,
    GetUsersCommandHandler,
)
from logic.commands.permissions import AccessCheckModeratorCommand, AccessCheckModeratorCommandHandler, AccessCheckUserCommand, AccessCheckUserCommandHandler
from logic.commands.users import (
    ConfirmCodeCommand,
    ConfirmCodeCommandHandler,
    SignInCommand,
    SignInCommandHandler,
    SignUpCommandHandler,
    SignUpCommand,
)
from logic.mediator import Mediator
from logic.services.auth import AuthService
from logic.services.senders import BaseSenderService, DummySenderService
from settings.config import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def create_sender_service() -> BaseSenderService:
        return DummySenderService()

    def create_user_cache() -> BaseUserCache:
        return MemoryUserCache()

    def create_auth_service() -> AuthService:
        settings: Settings = container.resolve(Settings)
        return AuthService(
            cache_client=create_user_cache(),
            sender_service=create_sender_service(),
            authJWT=settings.auth_jwt,
        )

    def create_user_repository() -> BaseUserRepository:
        return MemoryUserRepository()

    def create_chat_repository() -> BaseChatRepository:
        return MemoryChatRepository()

    def create_message_repository() -> BaseMessageRepository:
        return MemoryMessageRepository()

    # Register auth service
    container.register(AuthService, factory=create_auth_service, scope=Scope.singleton)
    # Register user repository
    container.register(
        BaseUserRepository, factory=create_user_repository, scope=Scope.singleton
    )
    # Register chat repository
    container.register(
        BaseChatRepository, factory=create_chat_repository, scope=Scope.singleton
    )
    # Reegister message repository
    container.register(
        BaseMessageRepository, factory=create_message_repository, scope=Scope.singleton
    )

    # Register command handlers
    container.register(SignUpCommandHandler)
    container.register(SignInCommandHandler)
    container.register(ConfirmCodeCommand)
    container.register(CreateChatCommand)
    container.register(GetUserChatsCommand)
    container.register(GetUserChatMessagesCommand)
    container.register(CreateMessageCommand)
    container.register(AddUserToChatCommand)
    container.register(GetUsersCommand)
    container.register(AccessCheckModeratorCommand)
    container.register(AccessCheckUserCommand)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # commands handlers
        sign_up_handler = SignUpCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )

        sign_in_handler = SignInCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )
        confirm_code_handler = ConfirmCodeCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )
        create_chat_handler = CreateChatCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            chat_repository=container.resolve(BaseChatRepository),
            auth_service=container.resolve(AuthService),
        )
        get_user_chats_handler = GetUserChatsCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            chat_repository=container.resolve(BaseChatRepository),
            auth_service=container.resolve(AuthService),
        )
        get_user_chat_messages_handler = GetUserChatMessagesCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            message_repository=container.resolve(BaseMessageRepository),
            auth_service=container.resolve(AuthService),
        )
        create_message_command_handler = CreateMessageCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            message_repository=container.resolve(BaseMessageRepository),
            auth_service=container.resolve(AuthService),
        )
        add_user_to_chat_command_handler = AddUserToChatCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            chat_repository=container.resolve(BaseChatRepository),
            auth_service=container.resolve(AuthService),
        )
        get_users_command_handler = GetUsersCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )
        access_check_moderator_command_handler = AccessCheckModeratorCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService)
        )
        access_check_user_command_handler = AccessCheckUserCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService)
        )


        # commands
        mediator.register_command(
            command=SignUpCommand, command_handlers=[sign_up_handler]
        )
        mediator.register_command(
            command=SignInCommand, command_handlers=[sign_in_handler]
        )
        mediator.register_command(
            command=ConfirmCodeCommand, command_handlers=[confirm_code_handler]
        )
        mediator.register_command(
            command=CreateChatCommand, command_handlers=[create_chat_handler]
        )
        mediator.register_command(
            command=GetUserChatsCommand, command_handlers=[get_user_chats_handler]
        )
        mediator.register_command(
            command=GetUserChatMessagesCommand,
            command_handlers=[get_user_chat_messages_handler],
        )
        mediator.register_command(
            command=CreateMessageCommand,
            command_handlers=[create_message_command_handler],
        )
        mediator.register_command(
            command=AddUserToChatCommand,
            command_handlers=[add_user_to_chat_command_handler],
        )
        mediator.register_command(
            command=GetUsersCommand,
            command_handlers=[get_users_command_handler],
        )
        mediator.register_command(
            command=AccessCheckModeratorCommand,
            command_handlers=[access_check_moderator_command_handler],
        )
        mediator.register_command(
            command=AccessCheckUserCommand,
            command_handlers=[access_check_user_command_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
