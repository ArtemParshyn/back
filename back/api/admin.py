from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from api.models import ApiUser, Reklama, Service, Category, Obzor

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Article

from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

admin.site.register(Article)
admin.site.register(ApiUser)
admin.site.register(Reklama)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Obzor)


class ArticlesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'
