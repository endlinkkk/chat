from domain.entities.users import Credentials, User
import pytest
from faker import Faker

from domain.values.users import Password, Phone, Username


@pytest.fixture
def user1(faker: Faker):
    username = Username(value=faker.text(max_nb_chars=20))
    password = Password(value="qwertyqwerty")
    phone = Phone(value="+79010010011")
    credentials = Credentials(phone=phone, password=password)
    return User(username=username, credentials=credentials)


@pytest.fixture
def user2(faker: Faker):
    username = Username(value=faker.text(max_nb_chars=20))
    password = Password(value="qwertyqwerty")
    phone = Phone(value="+79010010012")
    credentials = Credentials(phone=phone, password=password)
    return User(username=username, credentials=credentials)
