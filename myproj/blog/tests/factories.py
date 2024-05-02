# blog/tests/factories.py
#  - 반드시 blog/tests/__init__.py 빈 파일 먼저 생성해야만 팩키지로 인식

import factory
from accounts.tests.factories import UserFactory
from blog.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    author = factory.SubFactory(UserFactory)
