from django.shortcuts import render
from django.views import View
from accounts import models

class Index(View):
    context = {"title" : "صفحه اصلی"}
    def get(self , request):
        last_posts = models.Post.objects.all()[:3]
        self.context['last_posts'] = last_posts
        return render(request , "main/index.html" , context= self.context)
