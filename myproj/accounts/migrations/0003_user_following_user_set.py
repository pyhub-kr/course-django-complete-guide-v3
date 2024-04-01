# Generated by Django 4.2.11 on 2024-04-01 14:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="following_user_set",
            field=models.ManyToManyField(
                blank=True,
                related_name="follower_user_set",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
