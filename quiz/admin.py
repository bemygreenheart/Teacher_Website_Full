from django.contrib import admin
from django.utils.text import slugify

from .models import Quiz, Question, Option, Category

class OptionInline(admin.StackedInline):
  model = Option
  fields = (('is_answer', 'text'),)

  min_num = 2
  extra = 0
  max_num = 8


class QuestionManager(admin.ModelAdmin):
  model = Question
  inlines = [OptionInline,]

class QuizAdminManager(admin.ModelAdmin):
  exclude = ('slug', 'author')
  list_display = ('__str__', 'author', 'created_at')
  list_display_links = ('__str__',)
  date_hierarchy = 'created_at'
  ordering = ('-created_at',)
  search_fields = ['title']

  def save_model(self, request, obj, form, change):
    obj.slug = slugify(obj.title)
    obj.author = request.user
    super().save_model(request, obj, form, change)

admin.site.register(Quiz, QuizAdminManager)
admin.site.register(Question, QuestionManager)
admin.site.register(Category)

