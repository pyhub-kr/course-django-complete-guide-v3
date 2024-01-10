from django.conf import settings
from django.db import models


class ZipCode(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)


class JuniorEmployee(models.Model):
    id = models.IntegerField(primary_key=True, db_column="employee_id")
    first_name = models.CharField(max_length=50, db_column="employee_first_name")
    last_name = models.CharField(max_length=50, db_column="employee_last_name")

    class Meta:
        managed = False
        db_table = "junior_employee_view"


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shop_post_set",
    )
    message = models.TextField()
