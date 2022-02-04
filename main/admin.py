from django.contrib import admin
from accounts import models
# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Blog)
admin.site.register(models.Post)
