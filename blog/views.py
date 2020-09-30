from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Article, Comment, Category, Favorite
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import json
from django.http import JsonResponse


def article_list(request):
  articles= Article.objects.all()
  categories = Category.objects.all()
  keyword = request.GET.get('keyword', None)
  category = request.GET.get('category', None)
  month = request.GET.get('month', None)

  if keyword:
    articles = articles.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword))

  if category:
    articles = articles.filter(category__title=category)

  if month:
    month_y = month[:4]
    month_m= month[5:]
    articles = articles.filter(created_at__year = month_y, created_at__month=month_m )
  ctx = {'articles':articles, 'categories' :categories}
  return render(request, 'blog/latest.html', ctx)


def detail(request, id, slug):
  article = get_object_or_404(Article, id=id)
  comments = Comment.objects.filter(article=article)
  #  Sort favorites for the article and take count for each
  favs = Favorite.objects.all().filter(article=article)
  like_count = favs.filter(fav_type=1).count()
  dislike_count = favs.count() - like_count
  # Take the favorite type for the current user if any
  myfav_type = 0
  if request.user.is_authenticated:
    try:
      fav = Favorite.objects.get(article=article, owner=request.user)
      myfav_type = fav.fav_type 
    except Exception as e:
      pass

  ctx = {'article' : article,
    'comments' : comments,
    'like_count' : like_count,
    'dislike_count' : dislike_count,
    'myfav_type' : myfav_type}
  return render(request, 'blog/detail.html', ctx)


class FavoriteArticleView(LoginRequiredMixin, View):
  
  def post(self, request, id, slug):
    article = get_object_or_404(Article, id=id)
    req = json.loads(request.body.decode('utf-8'))
    fav_type = int(req['f_type'])
    try:
      fav = get_object_or_404(Favorite ,article = article, owner = request.user)
      if not fav_type == fav.fav_type:
        fav.fav_type = fav_type
        fav.save()
    except Exception as e: 
      fav = Favorite.objects.create(owner=request.user, article=article, fav_type=fav_type)
    
    t = fav.fav_type
    favs = Favorite.objects.filter(article=article)
    like_count = favs.filter(fav_type=1).count()
    unlike_count = favs.count() - like_count
    json_data = {
      'fav_type' : t,
      'like_count' : like_count,
      'dislike_count' : unlike_count,
    }
    return JsonResponse(json_data)


class UnfavoriteArticleView(LoginRequiredMixin, View):
  
  def post(self, request, id, slug):
    article = get_object_or_404(Article, id=id)
    req = json.loads(request.body.decode('utf-8'))
    fav_type = int(req['f_type'])
    try:
     fav = get_object_or_404(Favorite, owner=request.user, article=article)
     fav.delete()
    except  Exception as e:
      pass

    favs = Favorite.objects.filter(article=article)
    like_count = favs.filter(fav_type=1).count()
    unlike_count = favs.count() - like_count
    json_data = {
      'fav_type' : 0,
      'like_count' : like_count,
      'dislike_count' : unlike_count,
    }
    return JsonResponse(json_data)

class CommentView(LoginRequiredMixin, View):

  def post(self, request, id, slug):
    article = get_object_or_404(Article, id=id)
    comment = Comment(owner=request.user, article=article, text = request.POST.get('text', None))
    comment.save()
    return redirect(reverse('blog:detail', args =[id, slug]))