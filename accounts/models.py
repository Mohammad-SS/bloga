from django.db import models
from django.contrib.auth.models import User
import jdatetime as jdt


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    ban = models.BooleanField(default=False)
    access = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - ({self.phone_number}) "


def blog_media_uploader(instance, filename):
    return f"blogs/{instance.slug}/{filename}"


class Blog(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    slug = models.CharField(max_length=24, unique=True)
    title = models.CharField(max_length=24)
    banner = models.ImageField(upload_to=blog_media_uploader)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


def media_uploader(instance, filename):
    return f"blogs/{instance.blog.slug}/post_images/{filename}"


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField(blank=True, null=True)
    title = models.TextField()
    image = models.ImageField(upload_to=media_uploader, blank=True, null=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.title} - ({self.blog.slug}) "

    @property
    def persian_created_date(self):
        date = jdt.GregorianToJalali(self.created_date.year, self.created_date.month, self.created_date.day)
        return f"{date.jyear}/{date.jmonth}/{date.jday}"
