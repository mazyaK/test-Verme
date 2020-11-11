"""
Copyright 2020 ООО «Верме»
"""

import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db
]


def test_get_api_key_without_credentials(anon):
    anon.post(
        "/api/v1/auth/token/",
        expected_status_code=status.HTTP_400_BAD_REQUEST
    )


def test_get_api_key_with_wrong_password(make_user, test_password, test_password_2, anon):
    user = make_user(test_password)
    anon.post(
        "/api/v1/auth/token/",
        {"username": user.username, "password": test_password_2},
        expected_status_code=status.HTTP_400_BAD_REQUEST,
    )


def test_get_api_key_with_password(make_user, test_password, anon):
    user = make_user(test_password)
    response = anon.post(
        "/api/v1/auth/token/",
        {"username": user.username, "password": test_password},
        expected_status_code=status.HTTP_200_OK,
    )
    assert response == {"token": user.auth_token.key}
