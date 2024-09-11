from django.contrib import admin

from api.models import ApiUser, Reklama, Service, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Article

# Register your models here.
admin.site.register(ApiUser)
admin.site.register(Reklama)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Article)


class ArticlesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = '__all__'