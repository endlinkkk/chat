from application.api.moderator.decorators import handler_exceptions
from logic.commands.moderators import DeleteUserCommand
from logic.commands.permissions import AccessCheckModeratorCommand
from logic.init import init_container
from logic.mediator import Mediator

from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from punq import Container

router = APIRouter(tags=["Moderator"])
http_bearer = HTTPBearer()


@router.delete(
    "/",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Пользователь успешно удален"},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def delete_user_handler(
    user_oid: str,
    container: Container = Depends(init_container),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> None:
    mediator: Mediator = container.resolve(Mediator)
    token = credentials.credentials
    user, *_ = await mediator.handle_command(
        AccessCheckModeratorCommand(access_token=token)
    )
    await mediator.handle_command(DeleteUserCommand(moderator=user, user_oid=user_oid))
    return status.HTTP_204_NO_CONTENT
