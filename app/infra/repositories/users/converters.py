from domain.entities.users import Credentials, User
from domain.values.users import Password, Phone, Username
from infra.repositories.documents import CredentialsDocument, UserDocument


async def convert_user_document_to_entity(user_document: UserDocument) -> User:
    return User(
        username=Username(value=user_document["username"]),
        credentials=Credentials(
            phone=Phone(value=user_document["credentials"]["phone"]),
            password=Password(value=user_document["credentials"]["password"]),
            created_at=user_document["credentials"]["created_at"],
            oid=user_document["credentials"]["oid"],
        ),
        created_at=user_document["created_at"],
        oid=user_document["oid"],
        is_blocked=user_document["is_blocked"],
        is_confirmed=user_document["is_confirmed"],
        is_moderator=user_document["is_moderator"],
    )


async def convert_user_entity_to_document(user: User) -> UserDocument:
    return UserDocument(
        oid=user.oid,
        created_at=user.created_at,
        username=user.username.value,
        is_blocked=user.is_blocked,
        is_confirmed=user.is_confirmed,
        is_moderator=user.is_moderator,
        credentials=CredentialsDocument(
            phone=user.credentials.phone.value,
            password=user.credentials.password.value,
            created_at=user.credentials.created_at,
            oid=user.credentials.oid,
        ),
    )
