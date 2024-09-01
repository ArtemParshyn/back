from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/avatar', default=None)


class Reklama(models.Model):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/reklama', default=None)
    url = models.CharField(max_length=64)
