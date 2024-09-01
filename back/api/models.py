from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/', default=None)
