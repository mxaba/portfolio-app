from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .filters import PostFilter
from .forms import PostForm
from .models import Post, PostComment


def blog_home(request):
    posts = Post.objects.filter(active=True)

    my_filter = PostFilter(request.GET, queryset=posts)
    posts = my_filter.qs

    page = request.GET.get('page')

    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'my_filter': my_filter}
    return render(request, 'blog/blog_home.html', context)


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        comment = request.POST.get('comment')

        if len(comment) == 0:
            return redirect('blog:post-details', slug=post.slug)

        PostComment.objects.create(author=request.user, post=post, comment=comment)
        messages.success(request, "You're comment was successfully posted!")

        return redirect('blog:post-details', slug=post.slug)

    # posts = Post.objects.filter(active=True, featured=True).exclude(title=post.title)[:3]
    posts = Post.objects.filter(active=True, featured=True)[:3]

    context = {'post': post, 'posts': posts}
    return render(request, 'blog/post_details.html', context)


def user_posts(request, username):
    user = get_object_or_404(User, username=username)

    posts = Post.objects.filter(active=True, author=user)

    my_filter = PostFilter(request.GET, queryset=posts)
    posts = my_filter.qs

    page = request.GET.get('page')

    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'my_filter': my_filter, 'user': user}
    return render(request, 'blog/user_posts.html', context)


@login_required
def post_create(request):
    form = PostForm()

    print(request.method)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(form.is_valid())
        print(request.method)
        if form.is_valid():
            form.instance.author = request.user
            instance = form.save()
            return redirect('blog:post-details', slug=instance.slug)

    context = {'form': form, 'section_title': 'Add Post'}
    return render(request, 'blog/post_form.html', context)


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author == request.user:
        form = PostForm(instance=post)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                instance = form.save()
                messages.success(request, f'Post updated')
                return redirect('blog:post-details', slug=instance.slug)

        context = {'form': form, 'section_title': 'Update Post'}
        return render(request, 'blog/post_form.html', context)
    else:
        return HttpResponse('You are not authorized to edit this post.')


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author == request.user:
        if request.method == 'POST':
            post.delete()
            messages.success(request, f'Post deleted successfully')
            return redirect('blog:blog-home')

        context = {'post': post}
        return render(request, 'blog/post_confirm_delete.html', context)
    else:
        return HttpResponse('You are not authorized to delete this post.')
