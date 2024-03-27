from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string


class User(AbstractUser):
    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email/subject.txt")
        # 이메일 제목은 개행문자를 허용하지 않습니다.
        subject = " ".join(subject.splitlines())

        content = render_to_string(
            "accounts/welcome_email/content.txt",
            {
                "username": self.username,
            },
        )
        sender_email = settings.DEFAULT_FROM_EMAIL
        # TODO: celery, django-mailer 등을 통해 다른 프로세스를 통해 이메일 발송
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True)
