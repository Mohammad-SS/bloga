from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bloga import settings

# Create your views here.
from .helper import context_loader


class SignUp(View):
    def get(self, request):
        return render(request, "main/signup.html")

    def post(self, request):
        name = request.POST['name']
        phone = request.POST['mobile']
        national_id_number = request.POST['national_id']
        email = request.POST['email']
        password = request.POST['password']
        user = models.User.objects.filter(username=phone)
        if user.count() > 0:
            return render(request, "main/signup.html", {"errors": "کاربری با این شماره موبایل در حال حاضر موجود است ."})
        user = User.objects.create_user(username=phone, email=email, password=password)
        profile = models.Profile.objects.filter(national_id_number=national_id_number)
        if profile.count() > 0:
            return render(request, "main/signup.html", {"errors": "کاربری با این کدملی در حال حاضر موجود است ."})
        profile = models.Profile(user=user, full_name=name, national_id_number=national_id_number)
        profile.save()
        return redirect("login")


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return render(request, "main/login.html")

    def post(self, request):
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(username=phone, password=password)
        if user is None:
            return render(request, "main/login.html", {"errors": "کاربری با این مشخصات یافت نشد !"})
        else:
            login(request, user)
            return redirect("accounts:dashboard")


class Dashboard(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = context_loader(request.user)
            return render(request, "accounts/blogs.html", context)
        else:
            return redirect("accounts:login")


class NewBlog(View):
    def get(self, request):
        context = context_loader(request.user)
        return render(request, "accounts/create-blog.html", context)

    def post(self, request):
        profile = request.user.profile
        blog_name = request.POST['blog-name']
        special_chars = "!@#$%^&*()?><\"\':}{"
        slug = request.POST['slug']
        for c in slug:
            if c in special_chars:
                print(c)
                slug = slug.replace(c, "")
        slug = slug.strip()
        slug = slug.replace(" ", "-")
        title = request.POST['title']
        banner = request.FILES['banner']
        desc = request.POST['descriptions']
        notes = request.POST['user-note']
        blog = models.Blog.objects.filter(slug=slug)
        if blog.count():
            return render(request, "accounts/create-blog.html",
                          {"error": "وبلاگی با این نامک موجود است . لطفا نامک دیگری انتخاب کنید"})
        blog = models.Blog(profile=profile, slug=slug, name=blog_name, title=title, banner=banner, description=desc,
                           user_notes=notes)
        blog.save()
        return redirect("accounts:dashboard")


class BlogPage(View):

    def get(self, request, blog_slug):
        context = context_loader(request.user)
        context['blog'] = models.Blog.objects.get(profile=request.user.profile, slug=blog_slug)
        return render(request, "accounts/blog_page.html", context)


class BlogPosts(View):
    def get(self, request, blog_slug):
        context = context_loader(request.user)
        context['blog'] = models.Blog.objects.get(profile=request.user.profile, slug=blog_slug)
        context['posts'] = context['blog'].posts.order_by("-created_date")
        return render(request, "accounts/blog_posts.html", context)


class NewPost(View):
    def get(self, request, blog_slug):
        context = context_loader(request.user)
        return render(request, "accounts/new_post.html", context)

    def post(self, request, blog_slug):
        data = request.POST
        if "title" not in data:
            return HttpResponse("FAILE !")
        if "body" not in data:
            return HttpResponse("FAILE !")
        blog = models.Blog.objects.get(slug=blog_slug)
        if data["slug"]:
            slug = data['slug']
        else:
            slug = data['title']
        special_chars = "!@#$%^&*()?><\"\':}{"
        for c in slug:
            if c in special_chars:
                slug = slug.replace(c, "")
        slug = slug.strip()
        slug = slug.replace(" ", "-")
        does_slug_exist = models.Post.objects.filter(slug=slug, blog__slug=blog_slug)
        while does_slug_exist:
            slug = slug + "1"
            does_slug_exist = models.Post.objects.filter(slug=slug, blog__slug=blog_slug)
        post = models.Post(blog=blog, slug=slug, title=data['title'], body=data['body'], summary=data['summary'], )
        if "thumb" in request.FILES:
            post.image = request.FILES['thumb']
        post.save()

        return redirect("accounts:posts_page", blog_slug=blog_slug)


class EditPost(View):
    def get(self, request, blog_slug, post_id):
        context = context_loader(request.user)
        context['blog'] = models.Blog.objects.get(slug=blog_slug)
        context['post'] = models.Post.objects.get(pk=post_id)
        return render(request, "accounts/edit_post.html", context)

    def post(self, request, blog_slug, post_id):
        data = request.POST
        post = models.Post.objects.filter(pk=post_id)
        if "title" not in data:
            return HttpResponse("FAILE !")
        if "body" not in data:
            return HttpResponse("FAILE !")
        if "slug" in data:
            slug = data['slug']
        else:
            slug = data['title']
        special_chars = "!@#$%^&*()?><\"\':}{"
        for c in slug:
            if c in special_chars:
                slug = slug.replace(c, "")
        slug = slug.strip()
        slug = slug.replace(" ", "-")
        does_slug_exist = models.Post.objects.filter(slug=slug, blog__slug=blog_slug)
        while does_slug_exist:
            if does_slug_exist.count() == 1 and does_slug_exist[0].id == post_id:
                break
            slug = slug + "1"
            does_slug_exist = models.Post.objects.filter(slug=slug, blog__slug=blog_slug)

        updated = post.update(slug=slug, title=data['title'], body=data['body'], summary=data['summary'], )
        if "thumb" in request.FILES:
            post.image = request.FILES['thumb']

        return redirect("accounts:posts_page", blog_slug=blog_slug)


class DeletePost(View):
    def get(self, request, blog_slug, post_id):
        context = context_loader(request.user)
        context['blog'] = models.Blog.objects.get(slug=blog_slug)
        context['post'] = models.Post.objects.get(pk=post_id)
        return render(request, "accounts/delete_post.html", context)

    def post(self, request, blog_slug, post_id):
        post = models.Post.objects.filter(pk=post_id)
        post.delete()
        return redirect("accounts:posts_page", blog_slug=blog_slug)


def log_out(request):
    logout(request)
    return redirect("accounts:login")
