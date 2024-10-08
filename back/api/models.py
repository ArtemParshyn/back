from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class ApiUser(AbstractUser):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/avatar', default=None, blank=True)
    descr = models.CharField(max_length=128, default="Description", blank=True)
    can_create_articles = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.username


class Reklama(models.Model):
    choices = [("1", "first"), ("2", "second"), ("3", "third"), ("4", "index_popup"), ("5", "rotate1"),
               ("6", "rotate2"), ("7", "rotate3"), ("8", "rotate4"), ("9", "xlogo"), ("10", "header-button"), ("11", "main-banner"),
               ("12", "side_rotate1"), ("13", "side_rotate2"), ("14", "side_rotate3"), ("15", "side_rotate4")]
    pos_reklama = models.CharField(choices=choices, max_length=2)
    photo = models.ImageField(upload_to='images/%Y/%m/%d/reklama', default=None)
    url = models.URLField()
    button_text_index = models.CharField(max_length=20, default=None, blank=True)
    text_index = models.CharField(max_length=80, default=None, blank=True)
    tittle_index = models.CharField(max_length=45, default=None, blank=True)

    def __str__(self):
        return self.pos_reklama


class Category(models.Model):
    name = models.CharField(max_length=64)
    perevod = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Category_partner(models.Model):
    name = models.CharField(max_length=64)
    perevod = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Service(models.Model):
    photo = models.ImageField(upload_to='images/%Y/%m/%d/service')
    descr = models.CharField(max_length=256)
    promo = models.CharField(max_length=64, default=None, blank=True)
    website = models.URLField(blank=True, default=None)
    costs = models.CharField(max_length=64, default=None, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    to_index = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.descr


class Partner(models.Model):
    choices = [("1", "first"), ("2", "second"), ("3", "third"), ("4", "fourth"), ("5", "fifth")]
    photo = models.ImageField(upload_to='images/%Y/%m/%d/partner')
    descr = models.CharField(max_length=256)
    promo = models.CharField(max_length=64, default=None, blank=True)
    website = models.URLField(blank=True, default=None)
    costs = models.CharField(max_length=64, default=None, blank=True)
    category_partner = models.ForeignKey(Category_partner, on_delete=models.CASCADE, related_name="partners")
    pos = models.CharField(choices=choices, max_length=1, blank=True, default=None)  # Fixed here
    to_index = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.descr


class Article(models.Model):
    choices = [("1", "first"), ("2", "second"), ("3", "third")]

    image = models.ImageField(upload_to="images/%Y/%m/%d/preview", null=False, blank=False)  # Убрали default=None
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # Поле CKEditor
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_case = models.BooleanField(default=False, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=1, blank=True)
    is_draft = models.BooleanField(default=False)
    pos = models.CharField(choices=choices, blank=True, max_length=1, null=True)
    preview_for_index = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.title


class Obzor(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/obzor", null=False, blank=False)  # Убрали default=None
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # Поле CKEditor
    published_date = models.DateTimeField(auto_now_add=True)
    to_service = models.ForeignKey(Service, models.CASCADE, null=True, blank=True)  # Сделали ForeignKey необязательным

    def __str__(self):
        return self.title


class Obzor_partner(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/obzor", null=False, blank=False)  # Убрали default=None
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # Поле CKEditor
    published_date = models.DateTimeField(auto_now_add=True)
    to_partner = models.ForeignKey(Partner, models.CASCADE, null=True, blank=True)  # Сделали ForeignKey необязательным

    def __str__(self):
        return self.title
