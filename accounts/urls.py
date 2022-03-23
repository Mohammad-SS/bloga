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
from . import views

app_name = "accounts"
urlpatterns = [
    path("signup", views.SignUp.as_view(), name="signup"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("dashboard", views.Dashboard.as_view(), name="dashboard"),
    path("dashboard/new-blog", views.NewBlog.as_view(), name="new_blog"),
    path("dashboard/blogs/<str:blog_slug>", views.BlogPage.as_view(), name="blog_page"),
    path("dashboard/blogs/<str:blog_slug>/posts", views.BlogPosts.as_view(), name="posts_page"),
    path("dashboard/blogs/<str:blog_slug>/posts/new", views.NewPost.as_view(), name="new_post"),
    path("dashboard/blogs/<str:blog_slug>/posts/edit/<int:post_id>", views.EditPost.as_view(), name="edit_post"),
    path("dashboard/blogs/<str:blog_slug>/posts/delete/<int:post_id>", views.DeletePost.as_view(), name="delete_post"),

]
