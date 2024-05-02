# blog/tests/test_api.py

import base64

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from accounts.models import User
from accounts.tests.factories import UserFactory
from blog.models import Post
from blog.tests.factories import PostFactory


def create_user(raw_password: str = None) -> User:
    """새로운 User 레코드를 생성 및 반환"""
    return UserFactory(raw_password=raw_password)


def get_api_client_with_basic_auth(user: User, raw_password: str) -> APIClient:
    """인자의 User 인스턴스와 암호 기반에서 Basic 인증을 적용한 APIClient 인스턴스 반환"""

    # *.http 파일에서는 자동으로 base64 인코딩을 수행해줬었습니다.
    base64_data: bytes = f"{user.username}:{raw_password}".encode()
    authorization_header: str = base64.b64encode(base64_data).decode()

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Basic {authorization_header}")
    return client


@pytest.fixture
def unauthenticated_api_client() -> APIClient:
    """Authorization 인증 헤더가 없는 기본 APIClient 인스턴스 반환"""
    return APIClient()


@pytest.fixture
def api_client_with_new_user_basic_auth(faker) -> APIClient:
    """새로운 User 레코드를 생성하고, 그 User의 인증 정보가 Authorization 헤더로 지정된 APIClient 인스턴스 반환"""
    raw_password: str = faker.password()
    user: User = create_user(raw_password)
    api_client: APIClient = get_api_client_with_basic_auth(user, raw_password)
    return api_client


@pytest.fixture
def new_user() -> User:
    """새로운 User 레코드를 생성 및 반환"""
    return create_user()


@pytest.fixture
def new_post() -> Post:
    """새로운 Post 레코드를 반환"""
    return PostFactory()


def test_post_list():
    assert False
