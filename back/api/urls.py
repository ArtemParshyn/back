from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from api import views
from api.views import index, ProfileView
from back import settings

from .views import ArticleCreateView, UserArticleListView, enable_article_creation

urlpatterns = [
    path('', index),
    path('articles/', views.article_list, name='article_list'),
    #path('affiliatec', TemplateView.as_view(template_name='affiliatecasestudy.html')),
    #path('affiliatep', TemplateView.as_view(template_name='affiliate_program.html')),
    #path('article1', TemplateView.as_view(template_name='article_details.html')),
    path('services', views.services, name='services'),
    path('partners', views.partners, name='partners'),
    path('services/', views.services_add, name='services_add'),
    path('register', views.register, name="register"),
    path('login', views.loginu, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('createblog', views.createblog, name='createblog'),
    path('user_articles/', UserArticleListView.as_view(), name='user_articles'),
    path('create_blog', TemplateView.as_view(template_name='create_blog.html')),
    path('create/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('services_cat/', views.service_cat, name='services_cat'),
    path('partner_cat/', views.partner_cat, name='partner_cat'),
    path('obzor/<int:obzor_id>/', views.obzor_detail, name='obzor_detail'),
    path('obzorp/<int:obzor_id>/', views.obzorp_detail, name='obzorp_detail'),
    path('enable-article-creation/', enable_article_creation, name='enable_article_creation')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
