from . import models


def context_loader(user):
    profile = user.profile
    blogs = models.Blog.objects.filter(profile=profile, accepted=True)
    context = {"user": user, "profile": profile, "blogs": blogs}
    return context
