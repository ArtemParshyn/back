from django.contrib import admin

from api.models import ApiUser, Reklama, Service, Category

# Register your models here.
admin.site.register(ApiUser)
admin.site.register(Reklama)
admin.site.register(Service)
admin.site.register(Category)
