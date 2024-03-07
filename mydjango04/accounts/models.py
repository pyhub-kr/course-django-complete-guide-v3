import datetime

from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.model_fields import DatePickerField


def group_add_perm(self, perm_name: str) -> None:
    group = self
    app_label, codename = perm_name.split(".", 1)
    permission = Permission.objects.get(
        content_type__app_label=app_label,
        codename=codename,
    )
    # 그룹 퍼미션 목록에 추가
    group.permissions.add(permission)


# Group 클래스에 add_perm 메서드 추가하기
setattr(Group, "add_perm", group_add_perm)


class User(AbstractUser):
    # 친구 관계 (대칭 관계)
    friend_set = models.ManyToManyField(
        to="self",
        blank=True,
        # to="self"에서 디폴트 True
        symmetrical=True,
        # related_name="friend_set",
        related_query_name="friend_user",
    )

    # 팔로잉 관계 (비대칭 관계)
    follower_set = models.ManyToManyField(
        to="self",
        blank=True,
        # to="self"에서 디폴트 True
        symmetrical=False,
        # symmetrical=False 에서는 related_name을 지원
        related_name="following_set",
        related_query_name="following",
    )

    def add_perm(self, perm_name: str) -> None:
        # perm_name 예시 : "blog.add_post"

        user = self

        # app_label = "blog"
        # codename = "add_post"
        app_label, codename = perm_name.split(".", 1)

        # app_label과 codename으로 Permission 조회
        permission = Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename,
        )
        # 유저 퍼미션 목록에 추가
        user.user_permissions.add(permission)


@receiver(post_save, sender=User)
def post_save_on_user(instance: User, created: bool, **kwargs):
    if created:
        print(f"User({instance})의 프로필을 생성합니다.")
        Profile.objects.create(user=instance)


class SuperUserManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_superuser=True)


class SuperUser(User):
    objects = SuperUserManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_superuser = True
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    birth_date = DatePickerField(
        min_value=lambda: datetime.date.today(),
        max_value=lambda: datetime.date.today() + datetime.timedelta(days=7),
        blank=True,
        null=True,
    )
    address = models.CharField(max_length=100, blank=True)
    location_point = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[
            RegexValidator(
                r"^01\d[ -]?\d{4}[ -]?\d{4}$",
                message="휴대폰 번호 포맷으로 입력해주세요.",
            ),
        ],
    )
    point = models.PositiveIntegerField(default=0)  # 추가한 필드

    photo = models.ImageField(upload_to="profile/photo", blank=True)


@receiver(post_delete, sender=Profile)
def post_delete_on_profile(instance: Profile, **kwargs):
    instance.photo.delete(save=False)
