from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
import json

from .models import Quiz, Comment, Favorite, Category

def quiz_latest(request):
  quizes= Quiz.objects.all()
  categories = Category.objects.all()
  keyword = request.GET.get('keyword', None)
  category = request.GET.get('category', None)
  month = request.GET.get('month', None)

  if keyword:
    quizes = quizes.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword))

  if category:
    quizes = quizes.filter(category__title=category)

  if month:
    month_y = month[:4]
    month_m= month[5:]
    quizes = quizes.filter(created_at__year = month_y, created_at__month=month_m )
  ctx = {'quizes':quizes, 'categories' :categories}
  return render(request, 'quiz/latest.html', ctx)


def quiz_detail(request, id, slug):
  quiz = get_object_or_404(Quiz, id=id)
  comments = Comment.objects.filter(quiz=quiz)
  #  Sort favorites for the article and take count for each
  favs = Favorite.objects.all().filter(quiz=quiz)
  like_count = favs.filter(fav_type=1).count()
  dislike_count = favs.count() - like_count
  # Take the favorite type for the current user if any
  myfav_type = 0
  if request.user.is_authenticated:
    try:
      fav = Favorite.objects.get(quiz=quiz, owner=request.user)
      myfav_type = fav.fav_type 
    except Exception as e:
      pass

  ctx = {'quiz' : quiz,
    'comments' : comments,
    'like_count' : like_count,
    'dislike_count' : dislike_count,
    'myfav_type' : myfav_type}
  return render(request, 'quiz/detail.html', ctx)

  
class FavoriteQuizView(LoginRequiredMixin, View):
  
  def post(self, request, id, slug):
    quiz = get_object_or_404(Quiz, id=id)
    req = json.loads(request.body.decode('utf-8'))
    fav_type = int(req['f_type'])
    try:
      fav = get_object_or_404(Favorite ,quiz = quiz, owner = request.user)
      if not fav_type == fav.fav_type:
        fav.fav_type = fav_type
        fav.save()
    except Exception as e: 
      fav = Favorite.objects.create(owner=request.user, quiz=quiz, fav_type=fav_type)
    
    t = fav.fav_type
    favs = Favorite.objects.filter(quiz=quiz)
    like_count = favs.filter(fav_type=1).count()
    unlike_count = favs.count() - like_count
    json_data = {
      'fav_type' : t,
      'like_count' : like_count,
      'dislike_count' : unlike_count,
    }
    return JsonResponse(json_data)


class UnfavoriteQuizView(LoginRequiredMixin, View):
  
  def post(self, request, id, slug):
    quiz = get_object_or_404(Quiz, id=id)
    req = json.loads(request.body.decode('utf-8'))
    fav_type = int(req['f_type'])
    try:
     fav = get_object_or_404(Favorite, owner=request.user, quiz=quiz)
     fav.delete()
    except  Exception as e:
      pass

    favs = Favorite.objects.filter(quiz=quiz)
    like_count = favs.filter(fav_type=1).count()
    unlike_count = favs.count() - like_count
    json_data = {
      'fav_type' : 0,
      'like_count' : like_count,
      'dislike_count' : unlike_count,
    }
    return JsonResponse(json_data)

class QuizCommentView(LoginRequiredMixin, View):

  def post(self, request, id, slug):
    quiz = get_object_or_404(Quiz, id=id)
    comment = Comment(owner=request.user, quiz=quiz, text = request.POST.get('text', None))
    comment.save()
    return redirect(reverse('quiz:detail', args =[id, slug]))

def start(request):
  pass