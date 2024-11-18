from pytest import fixture


from infra.caches.users.base import BaseUserCache
from infra.repositories.messages.base import BaseChatRepository, BaseMessageRepository
from infra.repositories.users.base import BaseUserRepository
from logic.mediator import Mediator
from punq import Container

from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture(scope="function")
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture(scope="function")
def user_repository(container: Container) -> BaseUserRepository:
    return container.resolve(BaseUserRepository)


@fixture(scope="function")
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


@fixture(scope="function")
def message_repository(container: Container) -> BaseMessageRepository:
    return container.resolve(BaseMessageRepository)



@fixture(scope="function")
def user_cache(container: Container) -> BaseUserCache:
    return container.resolve(BaseUserCache)