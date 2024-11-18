from punq import Container, Scope

from infra.caches.users.base import BaseUserCache
from infra.caches.users.memory import MemoryUserCache
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from logic.init import _init_container





def init_dummy_container() -> Container:
    container = _init_container()


    def create_user_cache() -> BaseUserCache:
        return MemoryUserCache(
        )

    container.register(BaseUserRepository, MemoryUserRepository, scope=Scope.singleton)
    container.register(BaseUserCache, factory=create_user_cache, scope=Scope.singleton)
    return container
