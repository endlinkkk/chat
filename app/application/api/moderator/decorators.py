from functools import wraps

from fastapi import HTTPException, status

from domain.exceptions.base import ApplicationException
from logic.commands.permissions import AccessCheckModeratorCommand
from logic.mediator import Mediator


def handler_exceptions(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            token = kwargs['credentials'].credentials
            mediator: Mediator = kwargs['container'].resolve(Mediator)
            await mediator.handle_command(AccessCheckModeratorCommand(access_token=token))
            result = await handler(*args, **kwargs)
        except ApplicationException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": exception.message},
            )
        return result

    return wrapper
