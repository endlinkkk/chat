from datetime import datetime, timedelta
import random

from dataclasses import dataclass

from domain.entities.users import User
from infra.caches.users.base import BaseUserCache

import bcrypt
import jwt

from logic.services.senders import BaseSenderService
from settings.config import AuthJWT
from jwt.exceptions import DecodeError, InvalidTokenError


@dataclass
class AuthService:
    cache_client: BaseUserCache
    sender_service: BaseSenderService
    authJWT: AuthJWT

    async def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    async def generate_confirmation_code(self) -> str:
        return str(random.randint(100000, 999999))

    async def save_confirmation_code(self, user: User, code: str):
        await self.cache_client.add_code(phone=user.credentials.phone.value, code=code)

    async def send_code(self, user: User, code: str):
        await self.sender_service.send_code(user=user, code=code)

    async def check_confirmation_code(self, user: User, code: str) -> bool:
        return await self.cache_client.check_code(
            phone=user.credentials.phone.value, code=code
        )

    async def check_user_password(self, user: User, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), user.credentials.password.value)

    async def encode_jwt(self, user: User) -> str:
        now = datetime.now()
        payload = {
            "sub": user.oid,
            "username": user.username.value,
            "phone": user.credentials.phone.value,
            "exp": now + timedelta(minutes=self.authJWT.access_token_expire_minutes),
            "iat": now,
        }
        encoded = jwt.encode(
            payload=payload,
            key=self.authJWT.private_key_path.read_text(),
            algorithm=self.authJWT.algorithm,
        )
        return encoded

    async def decode_jwt(self, token: str) -> dict | None:
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self.authJWT.publick_key_path.read_text(),
                algorithms=[self.authJWT.algorithm],
            )
            return decoded
        except (DecodeError, InvalidTokenError):
            return None
