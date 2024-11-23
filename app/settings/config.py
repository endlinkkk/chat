import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent.parent
mongo_uri = os.getenv("MONGO_DB_CONNECTION_URI")


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    publick_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 120


class CacheConfig(BaseModel):
    cache_expire_seconds: int = 300
    cache_port: int = 6379
    cache_password: str = "root"
    cache_host: str = "cache"


class MongoConfig(BaseModel):
    mongodb_connection_uri: str = mongo_uri
    mongodb_database: str = "chat"
    mongodb_chat_collection: str = "chats"
    mongodb_message_collection: str = "messages"
    mongodb_user_collection: str = "users"


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    cache_config: CacheConfig = CacheConfig()
    mongo_config: MongoConfig = MongoConfig()
