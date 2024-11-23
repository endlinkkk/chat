from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection

from domain.entities.messages import Chat, Message
from domain.entities.users import User
from infra.repositories.documents import ChatDocument
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.messages.converters import (
    convert_chat_document_to_entity,
    convert_chat_entity_to_document,
    convert_message_document_to_entity,
    convert_message_entity_to_document,
)
from infra.repositories.users.converters import convert_user_document_to_entity
from settings.config import MongoConfig


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatRepository(BaseChatRepository, BaseMongoDBRepository):
    async def _get_user_by_user_oid(self, user_oid: str) -> User:
        user_document = await self.mongo_db_client[self.mongo_db_name][
            MongoConfig().mongodb_user_collection
        ].find_one(filter={"oid": user_oid})
        return await convert_user_document_to_entity(user_document)

    async def _get_message_by_message_oid(self, message_oid: str) -> Message:
        message_document = await self.mongo_db_client[self.mongo_db_name][
            MongoConfig().mongodb_message_collection
        ].find_one(filter={"oid": message_oid})
        return await convert_message_document_to_entity(message_document)

    async def add_chat(self, chat: Chat):
        await self._collection.insert_one(await convert_chat_entity_to_document(chat))

    async def get_chat_by_chat_oid(self, chat_oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={"oid": chat_oid})
        if chat_document:
            users = [
                await self._get_user_by_user_oid(user_oid)
                for user_oid in chat_document["users"]
            ]
            messages = [
                await self._get_message_by_message_oid(message_oid)
                for message_oid in chat_document["messages"]
            ]

            chat = await convert_chat_document_to_entity(chat_document)

            if users:
                chat.users = set(users)

            if messages:
                chat.messages = set(messages)

            return chat

    async def delete_chat_by_chat_oid(self, chat_oid):
        await self._collection.delete_one({"oid": chat_oid})

    async def get_chats_by_user_oid(self, user_oid) -> list[Chat]:
        chats = []
        chats_document = self._collection.find()
        async for chat_document in chats_document:
            for user_oid_ in chat_document["users"]:
                if user_oid_ == user_oid:
                    chats.append(await self.get_chat_by_chat_oid(chat_document["oid"]))
        return chats

    async def add_user_to_chat(self, user: User, chat: Chat):
        await self._collection.update_one(
            {"oid": chat.oid},
            {"$addToSet": {"users": user.oid}},
        )


@dataclass
class MongoDBMessageRepository(BaseMessageRepository, BaseMongoDBRepository):
    async def _add_message_oid_to_chat(
        self, chat_oid: str, message_oid: str
    ) -> ChatDocument:
        chat_collection: AgnosticCollection = self.mongo_db_client[self.mongo_db_name][
            MongoConfig().mongodb_chat_collection
        ]
        await chat_collection.update_one(
            {"oid": chat_oid}, {"$push": {"messages": message_oid}}
        )

    async def add_message(self, message: Message):
        await self._collection.insert_one(
            await convert_message_entity_to_document(message)
        )
        await self._add_message_oid_to_chat(
            chat_oid=message.chat_oid, message_oid=message.oid
        )

    async def get_message_by_message_oid(self, message_oid: str) -> Message:
        return await convert_message_document_to_entity(
            self._collection.find_one({"oid": message_oid})
        )

    async def get_messages_by_chat_oid(self, chat_oid) -> list[Message]:
        message_documents = self._collection.find()
        messages = []
        async for message_document in message_documents:
            if message_document["chat_oid"] == chat_oid:
                messages.append(
                    await convert_message_document_to_entity(message_document)
                )
        return messages
