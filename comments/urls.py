from django.urls import path
from . import views

urlpatterns = [
    # views ichida post_detail funksiyasi borligiga ishonch hosil qiling
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]