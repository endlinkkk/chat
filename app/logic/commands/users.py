from dataclasses import dataclass

from domain.entities.users import Credentials, User
from domain.values.users import Phone, Username, Password
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import (
    CodeNotVerifiedException,
    PasswordNotVerifiedException,
    ThisNumberIsAlreadyRegisteredException,
    UserNotConfirmedException,
    UserNotFoundException,
)
from logic.services.auth import AuthService


@dataclass(frozen=True)
class SignUpCommand(BaseCommand):
    username: str
    phone: str
    password: str


@dataclass(frozen=True)
class SignUpCommandHandler(BaseCommandHandler[SignUpCommand, None]):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: SignUpCommand):
        user = await self.user_repository.get_user_by_phone(phone=command.phone)
        if user is not None:
            raise ThisNumberIsAlreadyRegisteredException()

        password = Password(
            value=await self.auth_service.hash_password(command.password)
        )
        username = Username(value=command.username)
        phone = Phone(value=command.phone)
        credentials = Credentials(phone=phone, password=password)
        user = User(username=username, credentials=credentials)

        await self.user_repository.add_user(user=user)
        code = await self.auth_service.generate_confirmation_code()

        await self.auth_service.save_confirmation_code(user=user, code=code)

        await self.auth_service.send_code(user=user, code=code)


@dataclass(frozen=True)
class ConfirmCodeCommand(BaseCommand):
    phone: str
    code: str


@dataclass(frozen=True)
class ConfirmCodeCommandHandler(BaseCommandHandler[ConfirmCodeCommand, str]):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: ConfirmCodeCommand) -> str:
        user = await self.user_repository.get_user_by_phone(phone=command.phone)
        if not user:
            raise UserNotFoundException()

        if not await self.auth_service.check_confirmation_code(
            user=user, code=command.code
        ):
            raise CodeNotVerifiedException()

        await self.user_repository.confirm_user(user_oid=user.oid)

        token = await self.auth_service.encode_jwt(user)

        return token


@dataclass(frozen=True)
class SignInCommand(BaseCommand):
    phone: str
    password: str


@dataclass(frozen=True)
class SignInCommandHandler(BaseCommandHandler[ConfirmCodeCommand, str]):
    user_repository: BaseUserRepository
    auth_service: AuthService

    async def handle(self, command: SignInCommand) -> str:
        user = await self.user_repository.get_user_by_phone(phone=command.phone)

        if not user:
            raise UserNotFoundException()

        if user.is_confirmed is False:
            raise UserNotConfirmedException()

        if await self.auth_service.check_user_password(user, command.password) is False:
            raise PasswordNotVerifiedException()

        token = await self.auth_service.encode_jwt(user)

        return token
