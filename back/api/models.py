from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/avatar', default=None, blank=True)
    descr = models.CharField(max_length=128, default="Description", blank=True)


class Reklama(models.Model):
    choices = [("1", "first"), ("2", "second"), ("3", "third")]
    pos_reklama = models.CharField(choices=choices, max_length=1)
    photo = models.ImageField(upload_to='images/%Y/%m/%d/reklama', default=None)
    url = models.CharField(max_length=64)


class Service(models.Model):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/service')
    descr = models.CharField(max_length=256)
    promo = models.CharField(max_length=64, default=None, blank=True)
    website = models.URLField()
    costs = models.CharField(max_length=64, default=None, blank=True)
