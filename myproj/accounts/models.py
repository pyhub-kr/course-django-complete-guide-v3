from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following_user_set = models.ManyToManyField(
        "self",
        related_name="follower_user_set",
        symmetrical=False,
        blank=True,
    )

    def is_follower(self, to_user: "User") -> bool:
        return self.following_user_set.filter(id=to_user.id).exists()

    def follow(self, to_user: "User") -> None:
        self.following_user_set.add(to_user)

    def unfollow(self, to_user: "User") -> None:
        self.following_user_set.remove(to_user)

    def follower_count(self) -> int:
        return self.follower_user_set.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)
