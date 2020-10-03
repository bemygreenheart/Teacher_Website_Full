from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.quiz_latest, name ='latest'),
    path('<int:id>/<slug:slug>', views.quiz_detail, name='detail'),
    path('<int:id>/<slug:slug>/attempt', views.start, name ='start'),
]
