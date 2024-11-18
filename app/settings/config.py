from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    publick_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 120

class CacheConfig(BaseModel):
    cache_expire_seconds: int = 300
    cache_port: int = 6379
    cache_password: str = 'root'
    cache_host: str = 'cache'


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    cache_config: CacheConfig = CacheConfig()
    