from punq import Container, Scope

from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()

    container.register(BaseUserRepository, MemoryUserRepository, scope=Scope.singleton)

    return container
