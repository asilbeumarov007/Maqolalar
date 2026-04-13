from django import forms
from .models import Article, ArticleImage
from django.forms import inlineformset_factory

# Maqola va uning rasmlari orasidagi bog'liqlik formseti
ArticleImageFormSet = inlineformset_factory(
    Article,
    ArticleImage,
    fields=('image',),
    extra=1, # Yangi rasm qo'shish uchun 1 ta bo'sh joy
    can_delete=True # Rasmlarni o'chirish imkoniyati
)