from datetime import datetime
from pydantic import BaseModel, Field

from domain.entities.messages import Chat, Message
from domain.entities.users import User


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatResponseSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.value,
        )
    

class UserSchema(BaseModel):
    username: str
    user_oid: str

    @classmethod
    def from_entity(cls, user: User) -> 'UserSchema':
        return cls(
            username=user.username.value,
            user_oid=user.oid
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    participants: list[UserSchema]
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatDetailSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.value,
            created_at=chat.created_at,
            participants=[UserSchema(username=user.username.value, user_oid=user.oid) for user in chat.users]
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    sender_oid: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageDetailSchema":
        return MessageDetailSchema(
            oid=message.oid, text=message.text.value, created_at=message.created_at, sender_oid=message.sender_oid
        )


class GetUserChatsSchema(BaseModel):
    count: int
    chats: list[ChatDetailSchema] = Field(default_factory=list)


class GetUsersSchema(BaseModel):
    count: int
    users: list[UserSchema]


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str

    @classmethod
    def from_entity(cls, message: Message) -> "CreateMessageResponseSchema":
        return CreateMessageResponseSchema(oid=message.oid, text=message.text.value)


class CreateMessageSchema(BaseModel):
    text: str


class GetUserChatMessagesSchema(BaseModel):
    count: int
    messages: list[MessageDetailSchema] = Field(default_factory=list)
