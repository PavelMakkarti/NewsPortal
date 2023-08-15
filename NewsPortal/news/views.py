from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView

from .filters import PostFilter
from .forms import PostForm
from .models import Post

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .models import Subscriber, Category


class PostList(ListView):
    model = Post
    ordering = '-dataCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDeteil(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    raise_exception = True


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news.html')


class ArticlesCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticlesEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )