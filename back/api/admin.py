from django.contrib import admin
from api.models import ApiUser, Reklama, Service, Category, Obzor, Category_partner, Partner, Obzor_partner
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Article



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


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published', 'is_draft')
    list_filter = ('is_published', 'published_date', 'is_draft')
    actions = ['publish_articles', 'unpublish_articles']

    def publish_articles(self, request, queryset):
        rows_updated = queryset.update(is_published=True)
        self.message_user(request, f"{rows_updated} статьи были опубликованы.")

    def unpublish_articles(self, request, queryset):
        rows_updated = queryset.update(is_published=False)
        self.message_user(request, f"{rows_updated} статьи были сняты с публикации.")

admin.site.register(Article, ArticleAdmin)