from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.entities.users import User
from infra.repositories.messages.mongo import BaseMongoDBRepository
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.converters import (
    convert_user_document_to_entity,
    convert_user_entity_to_document,
)


from settings.config import MongoConfig


@dataclass
class MongoDBUserRepository(BaseMongoDBRepository, BaseUserRepository):
    async def _remove_user_from_chats(self, user_oid: str) -> list[Chat]:
        await self.mongo_db_client[self.mongo_db_name][
            MongoConfig().mongodb_chat_collection
        ].update_many({"users": user_oid}, {"$pull": {"users": user_oid}})

    async def add_user(self, user: User):
        await self._collection.insert_one(
            await convert_user_entity_to_document(user=user)
        )

    async def delete_user_by_user_oid(self, user_oid: str):
        await self._remove_user_from_chats(user_oid=user_oid)
        await self._collection.delete_one({"oid": user_oid})

    async def get_user_by_user_oid(self, user_oid: str) -> User | None:
        user_document = await self._collection.find_one({"oid": user_oid})
        if user_document:
            return await convert_user_document_to_entity(user_document)

    async def get_user_by_phone(self, phone: str) -> User | None:
        users_document = self._collection.find()
        async for user_document in users_document:
            if user_document["credentials"]["phone"] == phone:
                return await convert_user_document_to_entity(user_document)

    async def get_users(self, limit: int) -> list[User]:
        users_document = self._collection.find().limit(limit)
        users = [
            await convert_user_document_to_entity(user_document)
            async for user_document in users_document
        ]
        return users

    async def confirm_user(self, user_oid: str):
        filter_query = {"oid": user_oid}
        update_query = {"$set": {"is_confirmed": True}}
        await self._collection.update_one(filter_query, update_query)
