from application.api.messages.decorators import handler_exceptions
from application.api.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageSchema,
    GetUserChatMessagesSchema,
    GetUserChatsSchema,
    GetUsersSchema,
    MessageDetailSchema,
    UserSchema,
)
from domain.entities.users import User
from logic.commands.messages import (
    AddUserToChatCommand,
    CreateChatCommand,
    CreateMessageCommand,
    GetUserChatMessagesCommand,
    GetUserChatsCommand,
    GetUsersCommand,
)
from logic.commands.users import ConfirmCodeCommand, SignInCommand, SignUpCommand
from logic.init import init_container
from logic.mediator import Mediator

from fastapi.routing import APIRouter
from fastapi import Depends, WebSocket, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from punq import Container

router = APIRouter(tags=["Chat"])
http_bearer = HTTPBearer()


# Общие обработчики

# Создать чат
# Список своих чатов
# Посмотреть сообщений для конкретного чата
# Подключиться к чату по вебсокет
# Написать сообщение
# Удалить свой чат
# Удалить свое сообщение


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового чата для пользователя",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def create_user_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> CreateChatResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials

    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=schema.title, access_token=token)
    )

    return CreateChatResponseSchema.from_entity(chat=chat)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": GetUserChatsSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def get_user_chats_handler(
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials
    chats, *_ = await mediator.handle_command(GetUserChatsCommand(access_token=token))
    return GetUserChatsSchema(
        count=len(chats), chats=[ChatDetailSchema.from_entity(chat) for chat in chats]
    )


@router.get(
    "/{chat_oid}/messages/",
    responses={
        status.HTTP_200_OK: {"model": GetUserChatMessagesSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def get_chat_messages_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials
    messages, *_ = await mediator.handle_command(
        GetUserChatMessagesCommand(access_token=token, chat_oid=chat_oid)
    )
    return GetUserChatMessagesSchema(
        count=len(messages),
        messages=[MessageDetailSchema.from_entity(message) for message in messages],
    )


@router.post(
    "/{chat_oid}/messages/",
    response_model=CreateMessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового сообщения для пользователя",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema,
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> CreateChatResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials

    message, *_ = await mediator.handle_command(
        CreateMessageCommand(text=schema.text, chat_oid=chat_oid, access_token=token)
    )

    return CreateMessageResponseSchema.from_entity(message=message)


@router.post(
    "/{chat_oid}/add/",
    status_code=status.HTTP_200_OK,
    description="Добавление пользователя в чат",
    responses={
        status.HTTP_200_OK: {"description": "Пользователь добавлен в чат"},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },

)
@handler_exceptions
async def add_user_to_chat_handler(
    chat_oid: str,
    user_oid: str,
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> None:
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials
    await mediator.handle_command(
        AddUserToChatCommand(user_oid=user_oid, chat_oid=chat_oid, access_token=token)
    )


@router.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    description="Список пользователей",
    responses={
        status.HTTP_200_OK: {'model': GetUsersSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
        
    }
)
async def get_users_handler(
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> GetUsersSchema:
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials
    users, *_ = await mediator.handle_command(
        GetUsersCommand(access_token=token)
    )
    return GetUsersSchema(
        count=len(users),
        users=[UserSchema.from_entity(user) for user in users]
    )

# Обработчики для модератора

# Список всех чатов
# Получить все сообщения чата по oid
# Удалить сообщение по oid
# Заблокировать пользователя (Заблокированные пользователи не могут писать сообщения)


