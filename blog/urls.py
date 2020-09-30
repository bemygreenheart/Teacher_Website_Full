from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.article_list, name = 'latest'),
    path('<int:id>/<slug:slug>', views.detail, name = 'detail'),
    path('<int:id>/<slug:slug>/favorite', views.FavoriteArticleView.as_view(), name ='favorite'),
    path('<int:id>/<slug:slug>/unfavorite', views.UnfavoriteArticleView.as_view(), name = 'unfavorite'),
    path('<int:id>/<slug:slug>/comment', views.CommentView.as_view(), name='create_comment'),
]
