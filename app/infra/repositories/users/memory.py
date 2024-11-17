from dataclasses import dataclass, field


from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository


@dataclass
class MemoryUserRepository(BaseUserRepository):
    _saved_users: list[User] = field(default_factory=list, kw_only=True)

    async def add_user(self, user: User):
        self._saved_users.append(user)

    async def delete_user_by_user_oid(self, user_oid: str):
        for user in self._saved_users:
            if user.oid == user_oid:
                user.is_blocked = True
                break

    async def get_user_by_user_oid(self, user_oid: str) -> User | None:
        try:
            return next(user for user in self._saved_users if user.oid == user_oid)
        except StopIteration:
            return None

    async def get_user_by_phone(self, phone: str) -> User | None:
        try:
            user = next(
                user
                for user in self._saved_users
                if user.credentials.phone.value == phone
            )
            return user
        except StopIteration:
            return None

    async def get_users(self, limit: int) -> list[User]:
        return self._saved_users[:limit]
