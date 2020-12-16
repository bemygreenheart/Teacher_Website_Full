from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(template_name='index.html'), name='home' ),
    path('about', views.AboutTemplateView.as_view(), name='about' ),
    path('contact', views.ContactView.as_view(), name='contact' ),
    path('auth/login', views.login_user, name = 'login'),
    path('auth/signup', views.signup_user, name = 'signup'),
]
