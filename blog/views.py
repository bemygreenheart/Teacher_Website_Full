from django.shortcuts import render, get_object_or_404
from .models import Article, Comment

def article_list(request):
  articles= Article.objects.all()
  return render(request, 'blog/latest.html', {'articles':articles})

def detail(request, id, slug):
   article = get_object_or_404(Article, id=id)
   comments = Comment.objects.all().filter(article=article)
   ctx = {'article' : article, 'comments' : comments}
   return render(request, 'blog/detail.html', ctx)
