from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=200, blank=True)
    body = RichTextField(null=True, blank=True) # null=True qo'shildi
    photo = models.ImageField(upload_to='images/', blank=True)
    date = models.DateField(auto_now_add=True, null=True) # null=True qo'shildi
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True # null=True qo'shildi
    )
    # ... qolgan qismlar

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='articles/gallery/')

    def __str__(self):
        return f"{self.article.title} rasmi"