from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('quiz/', include('quiz.urls')),
]

if settings.DEBUG ==True:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    