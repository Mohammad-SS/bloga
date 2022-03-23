"""bloga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "main"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("search", views.SearchBlog.as_view(), name="search-blog"),
    path("blogs/<str:blog_slug>/", views.ShowBlog.as_view(), name="blog-page"),
    path("blogs/<str:blog_slug>/<str:post_slug>", views.ShowPost.as_view(), name="post-page"),

    path("upload_handler", csrf_exempt(views.PictureUpload), name="new_pic"),
]
