from django.contrib import admin
from api.models import ApiUser, Reklama, Service, Category, Obzor, Category_partner, Partner, Obzor_partner
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Article


admin.site.register(Article)
admin.site.register(ApiUser)
admin.site.register(Reklama)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Obzor)
admin.site.register(Category_partner)
admin.site.register(Partner)
admin.site.register(Obzor_partner)

class ArticlesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'
