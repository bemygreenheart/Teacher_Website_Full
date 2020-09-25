from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.article_list, name = 'latest'),
    path('<int:id>/<slug:slug>', views.detail, name = 'detail'),
]
