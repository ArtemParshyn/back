from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from api import views
from api.views import index, ProfileView
from back import settings

urlpatterns = [
    path('', index),
    path('articles', TemplateView.as_view(template_name='articles.html')),
    path('services', views.services, name='services'),
    path('services/', views.services_add, name='services_add'),
    path('register', views.register, name="register"),
    path('login', views.loginu, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('createblog', views.createblog, name='createblog'),
    path('services_cat/', views.service_cat, name='services_cat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
