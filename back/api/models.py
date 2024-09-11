from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class ApiUser(AbstractUser):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/avatar', default=None, blank=True)
    descr = models.CharField(max_length=128, default="Description", blank=True)


class Reklama(models.Model):
    choices = [("1", "first"), ("2", "second"), ("3", "third")]
    pos_reklama = models.CharField(choices=choices, max_length=1)
    photo = models.ImageField(upload_to='images/%Y/%m/%d/reklama', default=None)
    url = models.CharField(max_length=64)


class Article(models.Model):
    image = models.ImageField(null=False, blank=False, default=None)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # Поле CKEditor
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title