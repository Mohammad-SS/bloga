from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
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
        self.context['blogs'] = models.Blog.objects.filter(title__contains=query)
        return render(request, "main/show-search-result.html", context=self.context)


class ShowBlog(View):

    def get(self, request, blog_slug, **kwargs):
        if "page" in request.GET:
            page_number = int(request.GET['page'])
        else:
            page_number = 1
        posts_per_page = 10
        blog = get_object_or_404(models.Blog, slug=blog_slug)
        posts = blog.post_set.order_by("id")
        total_pages = int(posts.count() / posts_per_page)
        pages = range(0, total_pages + 1)
        print(posts_per_page * page_number)
        start_point = (page_number - 1) * posts_per_page
        posts = posts[start_point: start_point + posts_per_page]
        return render(request, "blogs/index.html", {"posts": posts, "blog": blog, "pages": pages})


class ShowPost(View):

    def get(self, request, blog_slug, post_slug):
        blog = get_object_or_404(models.Blog, slug=blog_slug)
        post = blog.post_set.get(slug=post_slug)

        return render(request, "blogs/single.html", {"blog": blog, "post": post})
