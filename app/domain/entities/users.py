from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.values.users import Phone, Username, Password


@dataclass(eq=False)
class User(BaseEntity):
    username: Username
    credentials: "Credentials"
    is_confirmed: bool = field(default=False, kw_only=True)
    is_blocked: bool = field(default=False, kw_only=True)
    is_moderator: bool = field(default=False, kw_only=True)


@dataclass(eq=False)
class Credentials(BaseEntity):
    phone: Phone
    password: Password
