from django.contrib import admin
from .models import Article, ArticleImage

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 3

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline]
    list_display = ['title']

