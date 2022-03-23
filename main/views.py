import jdatetime
import os

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
from bloga import settings
from django.core.files.storage import FileSystemStorage

from accounts import models


class Index(View):
    context = {"title": "صفحه اصلی"}

    def get(self, request):
        last_posts = models.Post.objects.all()[:3]
        self.context['last_posts'] = last_posts
        return render(request, "main/index.html", context=self.context)


class SearchBlog(View):
    context = {"title": "جست و جو"}

    def get(self, request):
        if not "search" in request.GET:
            return redirect("index")
        query = request.GET['search']
        self.context['blogs'] = models.Blog.objects.filter(title__contains=query, accepted=True)
        return render(request, "main/show-search-result.html", context=self.context)


class ShowBlog(View):

    def get(self, request, blog_slug, **kwargs):
        if "page" in request.GET:
            page_number = int(request.GET['page'])
        else:
            page_number = 1
        posts_per_page = 10
        blog = get_object_or_404(models.Blog, slug=blog_slug, accepted=True)
        posts = blog.posts.order_by("-created_date")
        total_pages = int(posts.count() / posts_per_page)
        pages = range(0, total_pages + 1)
        start_point = (page_number - 1) * posts_per_page
        posts = posts[start_point: start_point + posts_per_page]
        return render(request, "blogs/index.html", {"posts": posts, "blog": blog, "pages": pages})


class ShowPost(View):

    def get(self, request, blog_slug, post_slug):
        blog = get_object_or_404(models.Blog, slug=blog_slug)
        post = blog.posts.get(slug=post_slug)

        return render(request, "blogs/single.html", {"blog": blog, "post": post})


def PictureUpload(request):
    pic = request.FILES['file']
    user = request.user.id
    date = jdatetime.date.today()
    path = dict()
    path['private'] = os.path.join(settings.MEDIA_ROOT, str(user), str(date.year), str(date.month))
    fs = FileSystemStorage(path['private'])
    filename = fs.save(pic.name, pic)
    # file_url = fs.url(filename)
    # print(file_url)
    path['public'] = f'{settings.SITE_URL}{settings.MEDIA_URL}/{str(user)}/{str(date.year)}/{str(date.month)}/{filename}'
    return JsonResponse({"location": path['public']})
