from django.shortcuts import render, get_object_or_404
from .models import Article, Comment, Category
from django.db.models import Q

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
   comments = Comment.objects.all().filter(article=article)
   ctx = {'article' : article, 'comments' : comments}
   return render(request, 'blog/detail.html', ctx)

