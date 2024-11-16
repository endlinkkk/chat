from pytest import fixture

from domain.entities.messages import Chat
from domain.entities.users import Credentials, User
from domain.values.messages import Title
from domain.values.users import Password, Phone, Username


@fixture(scope="function")
def user() -> User:
    username = Username(value="user")
    phone = Phone(value="+79010000000")
    password = Password(value="alpine1212")
    crd = Credentials(phone=phone, password=password)
    user = User(username=username, credentials=crd, is_confirmed=True)

    return user


@fixture(scope="function")
def chat() -> Chat:
    return Chat(
        title=Title(value="mychat"),
    )


@fixture(scope='function')
def user2() -> User:
    username = Username(value="user2")
    phone = Phone(value="+79010000001")
    password = Password(value="alpine1212")
    crd = Credentials(phone=phone, password=password)
    user = User(username=username, credentials=crd, is_confirmed=True)

    return user


@fixture(scope='function')
def users() -> list[User]:
    users_list = []
    for i in range(5):
        username = Username(value=f"user{i}")
        phone = Phone(value=f"+7901000000{10-i}")
        password = Password(value="alpine1212")
        crd = Credentials(phone=phone, password=password)
        user = User(username=username, credentials=crd, is_confirmed=True)
        users_list.append(user)
    return users_list