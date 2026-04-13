from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required
from .forms import ArticleImageFormSet

# Ro'yxat ko'rinishi
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'

# MAQOLA DETALI VA IZOHLAR (FUNKSIYA ORQALI)
@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Maqolaga tegishli izohlarni olish
    comments = article.comments.all().order_by('-date_posted')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

# Tahrirlash
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo')
    template_name = 'article_edit.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['images'] = ArticleImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['images'] = ArticleImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        if images.is_valid():
            self.object = form.save()
            images.instance = self.object
            images.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.get_object().author == self.request.user

# O'chirish
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

# Yangi maqola yaratish
class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser