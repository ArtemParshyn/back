from django.contrib import admin

from api.models import ApiUser, Reklama, Service

# Register your models here.
admin.site.register(ApiUser)
admin.site.register(Reklama)
admin.site.register(Service)
