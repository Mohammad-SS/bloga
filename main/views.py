from django.shortcuts import render , redirect , HttpResponse , get_object_or_404
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

    def get(self , request):
        if not "search" in request.GET:
            return redirect("index")
        query = request.GET['search']
        self.context['blogs'] = models.Blog.objects.filter(title__contains=query)
        return render(request , "main/show-search-result.html" , context=self.context)


class ShowBlog(View):

    def get(self , request , blog_slug , **kwargs):
        blog = get_object_or_404(models.Blog,slug=blog_slug)
        return HttpResponse(blog_slug)
