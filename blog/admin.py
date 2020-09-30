from django.contrib import admin
from .models import Category, Article
from home.models import Reader

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  exclude = ('slug',)

  

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
  exclude = ('owner', 'slug')

  def save_model(self, request,obj, *args, **kwargs):
    obj.owner = request.user
    obj.save()

admin.site.register(Article, ArticleAdmin)

admin.site.register(Reader)