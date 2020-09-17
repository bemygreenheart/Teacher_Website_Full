from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(template_name='index.html'), name='home' ),
]
