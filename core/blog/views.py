from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from blog.models import BlogPost, Comment
from blog.forms import ProfileForm, BlogPostForm


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog.html')
    return render(request, "login.html")


def Profile(request):
    return render(request, "profile.html")


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert': alert})
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form': form})


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog.html", {'posts': posts})


@login_required(login_url='/login')
def add_blogs(request):
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html", {'obj': obj, 'alert': alert})
    else:
        form = BlogPostForm()
    return render(request, "add_blogs.html", {'form': form})


def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        comment = Comment(user=user, content=content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post': post, 'comments': comments})
