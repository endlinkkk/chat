from application.api.moderator.decorators import handler_exceptions
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

router = APIRouter(tags=["Moderator"])
http_bearer = HTTPBearer()


# Общие обработчики

# Создать чат
# Список своих чатов
# Посмотреть сообщений для конкретного чата
# Подключиться к чату по вебсокет
# Написать сообщение
# Удалить свой чат
# Удалить свое сообщение



@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"description": 'Mod'},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def delete_user_handler(
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials
    return "hi"