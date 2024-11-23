from application.api.users.decorators import handler_exceptions
from application.api.users.schemas import (
    ConfirmCodeRequestSchema,
    SignInRequestSchema,
    SignUpRequestSchema,
    TokenResponseSchema,
)
from logic.commands.users import ConfirmCodeCommand, SignInCommand, SignUpCommand
from logic.init import init_container
from logic.mediator import Mediator

from fastapi.routing import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi.security import HTTPBearer
from punq import Container

router = APIRouter(tags=["Auth"])
http_bearer = HTTPBearer()


@router.post(
    "/sign-up",
    description="Зарегистрировать пользователя с логином и паролем",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Пользователь успешно зарегистрирован",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def sign_up_handler(
    schema: SignUpRequestSchema, container: Container = Depends(init_container)
) -> str:
    mediator: Mediator = container.resolve(Mediator)
    await mediator.handle_command(
        SignUpCommand(
            username=schema.username, phone=schema.phone, password=schema.password1
        )
    )
    return f"Code is sent to {schema.phone}"


@router.post(
    "/confirm",
    description="Подтверждение регистрации пользователя",
    responses={
        status.HTTP_200_OK: {"model": TokenResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def confirm_handler(
    schema: ConfirmCodeRequestSchema, container: Container = Depends(init_container)
) -> TokenResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    token, *_ = await mediator.handle_command(
        ConfirmCodeCommand(phone=schema.phone, code=schema.code)
    )
    return TokenResponseSchema(
        access_token=token,
    )


@router.post(
    "/sign-in",
    description="Авторизоваться в системе",
    responses={
        status.HTTP_200_OK: {"model": TokenResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
    },
)
@handler_exceptions
async def sign_in_handler(
    schema: SignInRequestSchema,
    container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    token, *_ = await mediator.handle_command(
        SignInCommand(phone=schema.phone, password=schema.password)
    )
    return TokenResponseSchema(
        access_token=token,
    )


# @router.post(
#     "/send-code",
#     description="Отправить код повторно",
#     responses={
#         status.HTTP_200_OK: {"description": "Код успешно отправлен"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
#     },
# )
# @handler_exceptions
# async def send_code_handler(): ...


# @router.post(
#     "/logout",
#     description="Выход из аккаунта",
#     responses={
#         status.HTTP_200_OK: {"description": "Успешный выход"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
#     },
# )
# async def logout_handler(): ...


# @router.post(
#     "/reset-password",
#     description="Сброс пароля",
#     responses={
#         status.HTTP_200_OK: {"description": "Инструкция по сбросу пароля отправлена"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
#     },
# )
# async def reset_password_handler(): ...


# @router.post(
#     "/confirm-reset",
#     description="Подтверждение сброса пароля",
#     responses={
#         status.HTTP_200_OK: {"description": "Пароль успешно сброшен"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
#     },
# )
# async def confirm_reset_handler(): ...


# @router.patch(
#     "/update-password",
#     description="Обновить пароль",
#     responses={
#         status.HTTP_200_OK: {"description": "Пароль успешно обновлен"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
#     },
# )
# async def update_password_handler(): ...


# @router.post(
#     "/refresh-tokens",
#     description="Получить свежую пару токенов",
#     responses={
#         status.HTTP_200_OK: {"description": "Токены успешно обновлены"},
#         status.HTTP_400_BAD_REQUEST: {"description": "Что-то пошло не так"},
#     },
# )
# async def refresh_tokens_handler(): ...
