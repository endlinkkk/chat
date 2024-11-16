from pytest import fixture


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


# @fixture(scope="function")
# def chats_repository(container: Container) -> BaseChatsRepository:
#     return container.resolve(BaseChatsRepository)
