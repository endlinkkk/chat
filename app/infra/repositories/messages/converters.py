from domain.entities.messages import Chat, Message
from domain.values.messages import Text, Title
from infra.repositories.documents import (
    ChatDocument,
    MessageDocument,
)


async def convert_chat_entity_to_document(chat: Chat) -> ChatDocument:
    return ChatDocument(
        oid=chat.oid,
        title=chat.title.value,
        created_at=chat.created_at,
        users=[user.oid for user in chat.users],
        messages=[message.oid for message in chat.messages],
    )


async def convert_chat_document_to_entity(chat_document: ChatDocument) -> Chat:
    return Chat(
        title=Title(value=chat_document["title"]),
        oid=chat_document["oid"],
        created_at=chat_document["created_at"],
        users=set(user_oid for user_oid in chat_document["users"]),
        messages=set(message_oid for message_oid in chat_document["messages"]),
    )


async def convert_message_document_to_entity(
    message_document: MessageDocument,
) -> Message:
    return Message(
        text=Text(value=message_document["text"]),
        sender_oid=message_document["sender_oid"],
        chat_oid=message_document["chat_oid"],
        oid=message_document["oid"],
        created_at=message_document["created_at"],
    )


async def convert_message_entity_to_document(message: Message) -> MessageDocument:
    return MessageDocument(
        oid=message.oid,
        created_at=message.created_at,
        text=message.text.value,
        chat_oid=message.chat_oid,
        sender_oid=message.sender_oid,
    )
