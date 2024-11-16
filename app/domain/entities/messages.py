from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.entities.users import User
from domain.values.messages import Text, Title


@dataclass(eq=False)
class Message(BaseEntity):
    text: Text
    sender_oid: str
    chat_oid: str


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)
    users: set[User] = field(default_factory=set, kw_only=True)

    def add_message(self, message: Message):
        self.messages.add(message)

    def add_user(self, user: User):
        self.users.add(user)

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        return Chat(title=title)
