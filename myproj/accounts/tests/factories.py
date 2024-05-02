# accounts/tests/factories.py
#  - 반드시 accounts/tests/__init__.py 빈 파일 먼저 생성해야만 팩키지로 인식

import factory
from django.contrib.auth.hashers import make_password
from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")

    # UserFactory 인스턴스 생성 시에, 암호 입력을 지원하기 위함
    # raw_password 필드가 아니라 password 필드로 지정하면, 암호화없이 입력값 그대로 저장됩니다.
    raw_password = factory.Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # raw_password 필드값을 암호화하여 password 필드에 저장합니다.
        # User 모델에는 raw_password 이름의 필드가 없으므로 kwargs 사전에서 제거해줘야만 합니다.
        raw_password = kwargs.pop("raw_password", None)
        if raw_password:
            kwargs["password"] = make_password(raw_password)

        return super()._create(model_class, *args, **kwargs)
