from django.template.context_processors import static
from django.urls import path
from django.views.generic import TemplateView

from api import views
from api.views import index
from back import settings

urlpatterns = [
    path('', index),
    path('articles', TemplateView.as_view(template_name='articles.html')),
    path('profile', TemplateView.as_view(template_name='profile_main.html')),
    path('affiliatec', TemplateView.as_view(template_name='affiliatecasestudy.html')),
    path('affiliatep', TemplateView.as_view(template_name='affiliate_program.html')),
    path('services', TemplateView.as_view(template_name='services.html')),
    path('register', views.register, name="register"),
    path('login', views.loginu, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('createblog', views.createblog, name='createblog'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
