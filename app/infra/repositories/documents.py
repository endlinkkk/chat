from datetime import datetime
from typing import TypedDict


class CredentialsDocument(TypedDict):
    phone: str
    password: str
    oid: str
    created_at: datetime


class UserDocument(TypedDict):
    oid: str
    created_at: datetime
    username: str
    credentials: CredentialsDocument
    is_confirmed: bool
    is_blocked: bool
    is_moderator: bool


class MessageDocument(TypedDict):
    oid: str
    created_at: datetime
    text: str
    sender_oid: str
    chat_oid: str


class ChatDocument(TypedDict):
    oid: str
    title: str
    created_at: datetime
    messages: list[str]
    users: list[str]
