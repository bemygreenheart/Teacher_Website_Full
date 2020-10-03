from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.utils.text import slugify

FAV_CHOICES = ((1, 'LIKE'), (2, 'DISLIKE'))

class Category(models.Model):
  title = models.CharField(max_length=150, null=False, blank=False, unique=True)
  slug = models.SlugField(null = False, blank=True)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    return super(Category, self).save()

  def __str__(self):
    return self.title 


class Quiz(models.Model):
  title = models.CharField(max_length=250)
  slug = models.SlugField(null=False, blank=True)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.DO_NOTHING, related_name='quizes')
  image = models.ImageField(null = True, blank=True, upload_to = 'quiz')
  comments = models.ManyToManyField(AUTH_USER_MODEL, through='Comment', related_name='quiz_comments')
  categories = models.ManyToManyField(Category, related_name = 'category_quizes')
  favorites = models.ManyToManyField(AUTH_USER_MODEL, through='Favorite', related_name='favtorite_quizes')
  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    return super(Quiz, self).save(*args, **kwargs)

  def __str__(self):
    if len(self.title) > 30:
      return self.title[:27] + '...'
    return self.title


class Question(models.Model):
  text = models.TextField()
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions') 

  def __str__(self):
    if len(self.text) > 30:
      return self.text[:27]+'...'
    return self.text


class Option(models.Model):
  text = models.TextField()
  is_answer = models.BooleanField(default=False)
  question = models.ForeignKey(Question, on_delete=models.CASCADE ,related_name='options')

  def __str__(self):
    if len(self.text) > 30:
      return self.text[:27]+'...'
    return self.text


class Comment(models.Model):
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Favorite(models.Model):
  fav_type = models.IntegerField(choices=FAV_CHOICES)
  owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_quizes')
  quiz = models.ForeignKey(Quiz, on_delete = models.DO_NOTHING)

  class Meta:
    unique_together = ['owner', 'quiz']

  def __str__(self):
    mid = 'likes'
    if self.fav_type == 2:
      mid = 'dislikes'
    return self.owner + mid + self.quiz
