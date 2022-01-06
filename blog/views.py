from .models import Post, Comment, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.generic import (ListView,
                                  DetailView, CreateView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


def category_related(request, id):
    categories = Category.objects.all()
    posts = Post.objects.filter(category__pk=id)
    return render(request, 'index.html', {'posts': posts, 'categories': categories})


class CategoryRelated(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        id = self.kwargs.get('id')
        return Post.objects.filter(category__pk=id).order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.image = self.request.FILES['image']
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        user = get_user_model().objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('post_detail', slug=slug)
    return redirect('post_detail', slug=slug)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', ]
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(author=user).order_by('-create_at')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['title']
    template_name = 'category_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = '/blog/categories'

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'dashboard.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-create_at')
