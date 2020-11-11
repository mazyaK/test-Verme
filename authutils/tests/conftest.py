"""
Copyright 2020 ООО «Верме»
"""

import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def test_password():
    return "password"


@pytest.fixture()
def test_password_2():
    return "password2"


@pytest.fixture()
def make_user(mixer, test_password):
    def _user_generator(password=test_password, **kwargs):
        user = mixer.blend(User, **kwargs)
        user.set_password(password)
        user.save()
        return user
    return _user_generator
