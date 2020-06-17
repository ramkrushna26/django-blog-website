from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    context = {
        'post_s': Post.objects.all()
    }
    return render(request, 'posts/home.html', context)


@login_required
def postCreate(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, f'Post Created')
        return redirect(instance.get_absolute_url())
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def postUpdate(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.author != request.user:
        messages.success(request, f'You are not authorized to update this post.')
        return redirect(post.get_absolute_url())

    if request.POST:
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, f'Post Updated')
            return redirect(instance.get_absolute_url())
        else:
            form = PostForm(instance=post)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_update.html', {'form': form, 'post': post})


def addComment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.POST:
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            return redirect('posts-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment.html', {'form': form})

"""
@login_required
def approveComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.comment_approve()
    messages.success(request, f'Comment Approved')
    return redirect('posts-detail', pk=post_pk)
"""

@login_required
def deleteComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, f'Comment Deleted')
    return redirect('posts-detail', pk=post_pk)


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


class UserPostsView(ListView):
    model = Post
    template_name = 'posts/user_posts.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'post_s'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-posted_on')


class PostListView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = 'post_s'
    ordering = ['-posted_on']


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailView(DetailView):
    model = Post
    ordering = ['-commented_on']

