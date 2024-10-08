from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post
from .forms import PostForm


@login_required(login_url='/users/login/')
def home_page(request):
    return render(request,
                  template_name="app_main/home.html")

@login_required(login_url='/users/login/')
def users_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'app_main/users.html', context)


@login_required(login_url='/users/login')
def my_posts(request):
    my_posts = Post.objects.filter(owner=request.user)

    context = {
        'my_posts': my_posts
    }
    return render(request, 'app_main/my_post.html', context)


def all_posts(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'app_main/post.html', context)


@login_required(login_url='/users/login/')
def post_create(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            messages.success(request, "Post created successfully")
            return redirect("/")
        else:
            messages.error(request, "Form filled incorrectly")
            return redirect("/new-posts/")

    context = {
        'form': form
    }
    return render(request, 'app_main/post_form.html', context)

@login_required(login_url='login')
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.owner != request.user:
        messages.error(request, 'You cannot update other users\' posts')
        return redirect('home')

    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
            return redirect('home')
        else:
            messages.error(request, 'Form filled incorrectly')
            return redirect('post_update', kwargs={'post_id': post_id})

    context = {
        'form': form,
        'btn_text': 'Yangilash',
    }
    return render(request, 'app_main/post_form.html', context)


@login_required(login_url='login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.owner != request.user:
        messages.error(request, 'You cannot delete other users\'s posts')
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post successfully deleted')
        return redirect('home')


    context = {
        'post': post,
    }
    return render(request, 'app_main/post_delete.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post,
    }

    return render(request, "app_main/post_detail.html", context)


