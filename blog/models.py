from django.db import models
from django.utils.text import slugify
from django.conf.global_settings import AUTH_USER_MODEL

FAV_CHOICES = ((1, 'LIKE'), (2, 'DISLIKE'))

class Category(models.Model):
  title = models.CharField(max_length=150, null=False, blank=False, unique=True)
  slug = models.SlugField(null = False, blank=True)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    return super(Category, self).save()

  def __str__(self):
    return self.title

class Article(models.Model):
  title = models.CharField(max_length=255, null=False, blank=False)
  slug = models.SlugField(null=False)
  image = models.ImageField(upload_to = 'articles', null=True, blank= True)
  text = models.TextField()
  created_at= models.DateTimeField("time created" ,auto_now_add=True)
  updated_at = models.DateTimeField("last updated", auto_now=True)
  owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
  comments = models.ManyToManyField(AUTH_USER_MODEL, through='Comment', related_name='my_comments')
  favorites = models.ManyToManyField(AUTH_USER_MODEL, through='Favorite', related_name='my_favorites')
  category = models.ManyToManyField(Category, related_name='category_articles')

  def save(self, *args, **kwargs):
    self.slug= slugify(self.title)
    return super(Article, self).save(*args, **kwargs)

  def __str__(self):
    if len(self.title) > 20:
      return self.title[:17]+'...'
    return self.title


class Comment(models.Model):
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='favorite_blogs')
  article = models.ForeignKey(Article, on_delete=models.CASCADE)

class Favorite(models.Model):
  fav_type = models.IntegerField(choices=FAV_CHOICES)
  owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
  article = models.ForeignKey(Article, on_delete = models.DO_NOTHING)
