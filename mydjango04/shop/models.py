from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


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
        related_query_name="shop_post",
    )
    message = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)


class Order(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        # 가용한 제품에 대한 주문만 생성토록 제한합니다.
        # limit_choices_to={"is_available": True},
        limit_choices_to=Q(is_available=True),
    )


class Event(models.Model):
    name = models.CharField(max_length=100)
    event_date = models.DateField()


def get_current_date():
    return {"event_date__gte": timezone.now()}


class Ticket(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        limit_choices_to=get_current_date,
    )
