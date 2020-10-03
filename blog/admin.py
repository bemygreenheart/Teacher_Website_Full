from django.contrib import admin
from .models import Category, Article
from home.models import Reader

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  exclude = ('slug',)

  

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
  exclude = ('owner', 'slug')

  def save_model(self, request,obj, form, change):
    obj.owner = request.user
    super().save_model(request, obj, form, change)

admin.site.register(Article, ArticleAdmin)

admin.site.register(Reader)