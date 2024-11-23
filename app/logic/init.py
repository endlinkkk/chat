from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from infra.caches.users.base import BaseUserCache
from infra.caches.users.redis import RedisUserCache
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.messages.memory import (
    MemoryChatRepository,
    MemoryMessageRepository,
)
from infra.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessageRepository,
)
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from infra.repositories.users.mongo import MongoDBUserRepository
from infra.websockets.managers import BaseConnectionManager, ConnectionManager
from logic.commands.messages import (
    AddUserToChatCommand,
    AddUserToChatCommandHandler,
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
    GetChatCommand,
    GetChatCommandHandler,
    GetUserChatMessagesCommand,
    GetUserChatMessagesCommandHandler,
    GetUserChatsCommand,
    GetUserChatsCommandHandler,
    GetUsersCommand,
    GetUsersCommandHandler,
)
from logic.commands.moderators import DeleteUserCommand, DeleteUserCommandHandler
from logic.commands.permissions import (
    AccessCheckModeratorCommand,
    AccessCheckModeratorCommandHandler,
    AccessCheckUserCommand,
    AccessCheckUserCommandHandler,
)
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

from redis.asyncio import Redis
from motor.motor_asyncio import AsyncIOMotorClient


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    settings: Settings = container.resolve(Settings)

    def create_mongodb_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            settings.mongo_config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )

    container.register(
        AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton
    )

    mongo_client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongodb_repository() -> BaseChatRepository:
        return MongoDBChatRepository(
            mongo_db_client=mongo_client,
            mongo_db_name=settings.mongo_config.mongodb_database,
            mongo_db_collection_name=settings.mongo_config.mongodb_chat_collection,
        )

    def init_message_mongodb_repository() -> BaseMessageRepository:
        return MongoDBMessageRepository(
            mongo_db_client=mongo_client,
            mongo_db_name=settings.mongo_config.mongodb_database,
            mongo_db_collection_name=settings.mongo_config.mongodb_message_collection,
        )

    def init_user_mongodb_repository() -> BaseUserRepository:
        return MongoDBUserRepository(
            mongo_db_client=mongo_client,
            mongo_db_name=settings.mongo_config.mongodb_database,
            mongo_db_collection_name=settings.mongo_config.mongodb_user_collection,
        )

    def create_sender_service() -> BaseSenderService:
        return DummySenderService()

    def create_redis_client():
        return Redis(
            host=settings.cache_config.cache_host,
            port=settings.cache_config.cache_port,
            password=settings.cache_config.cache_password,
        )

    container.register(Redis, factory=create_redis_client, scope=Scope.singleton)

    redis_client = container.resolve(Redis)

    def create_user_cache() -> BaseUserCache:
        return RedisUserCache(
            redis_client=redis_client, cache_config=settings.cache_config
        )

    def create_auth_service() -> AuthService:
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
        BaseUserRepository, factory=init_user_mongodb_repository, scope=Scope.singleton
    )
    # Register chat repository
    container.register(
        BaseChatRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton
    )
    # Reegister message repository
    container.register(
        BaseMessageRepository,
        factory=init_message_mongodb_repository,
        scope=Scope.singleton,
    )
    # Register user cache
    container.register(BaseUserCache, factory=create_user_cache, scope=Scope.singleton)

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
    container.register(DeleteUserCommand)
    container.register(GetChatCommand)

    # Message Broker

    container.register(
        BaseConnectionManager, instance=ConnectionManager(), scope=Scope.singleton
    )

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
        )
        get_user_chats_handler = GetUserChatsCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            chat_repository=container.resolve(BaseChatRepository),
        )
        get_user_chat_messages_handler = GetUserChatMessagesCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            message_repository=container.resolve(BaseMessageRepository),
        )
        create_message_command_handler = CreateMessageCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            message_repository=container.resolve(BaseMessageRepository),
        )
        add_user_to_chat_command_handler = AddUserToChatCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            chat_repository=container.resolve(BaseChatRepository),
        )
        get_users_command_handler = GetUsersCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
        )
        access_check_moderator_command_handler = AccessCheckModeratorCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )
        access_check_user_command_handler = AccessCheckUserCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )
        delete_user_command_handler = DeleteUserCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            auth_service=container.resolve(AuthService),
        )
        get_chat_command_handler = GetChatCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            chat_repository=container.resolve(BaseChatRepository),
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
        mediator.register_command(
            command=DeleteUserCommand,
            command_handlers=[delete_user_command_handler],
        )
        mediator.register_command(
            command=GetChatCommand, command_handlers=[get_chat_command_handler]
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
