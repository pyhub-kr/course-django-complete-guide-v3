from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from accounts.models import User


def send_welcome_email(user: User, fail_silently=False):
    if user.email:
        subject = render_to_string("accounts/welcome_email/subject.txt", {})
        subject = " ".join(subject.splitlines())

        content = render_to_string(
            "accounts/welcome_email/content.txt",
            {
                "username": user.username,
            },
        )
        sender = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, content, sender, recipient_list, fail_silently=fail_silently)
