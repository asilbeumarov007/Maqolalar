from django.shortcuts import render, get_object_or_404, redirect
from articles.models import Article  # Boshqa ilovadan import qilish
from .models import Comment
from .forms import CommentForm


def post_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Izohlarni maqolaga bog'langan holda olish
    comments = Comment.objects.filter(post__pk=article.pk).order_by('-date_posted')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post  # Modelga mosligini tekshiring
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'comments/post_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })