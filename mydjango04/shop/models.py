from django.db import models


class ZipCode(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
