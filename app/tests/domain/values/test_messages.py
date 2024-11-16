from datetime import datetime
from domain.entities.messages import Message
from domain.entities.users import User
from domain.exceptions.messages import EmptyTextException
from domain.values.messages import Text

import pytest
from faker import Faker


def test_create_message_success(user1: User, user2: User, faker: Faker):
    text = Text(faker.text(max_nb_chars=254))
    message = Message(text=text, sender_oid=user1.oid, recipient_oid=user2.oid)

    assert message.text == text
    assert message.sender_oid == user1.oid
    assert message.recipient_oid == user2.oid
    assert message.created_at.date() == datetime.today().date()


def test_create_empty_message_text():
    with pytest.raises(EmptyTextException):
        Text("")
