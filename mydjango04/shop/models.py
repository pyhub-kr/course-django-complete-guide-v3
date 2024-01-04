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
