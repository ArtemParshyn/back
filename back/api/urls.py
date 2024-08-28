from django.template.context_processors import static
from django.urls import path
from django.views.generic import TemplateView

from back import settings

urlpatterns = [
    path("", TemplateView.as_view(template_name='index.html')),
    path("articles", TemplateView.as_view(template_name='articles.html')),
    path("affiliatec", TemplateView.as_view(template_name='affiliatecasestudy.html')),
    path("affiliatep", TemplateView.as_view(template_name='affiliate_program.html')),
    path("services", TemplateView.as_view(template_name='services.html')),
]

