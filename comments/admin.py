from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 'post' o'rniga 'article', 'user' o'rniga 'author' yozamiz
    list_display = ['author', 'article', 'date_posted']