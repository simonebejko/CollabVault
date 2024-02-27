from django.conf import settings
from django.db import models
from django.utils.text import slugify
from collabvault.utils.generators import unique_slugify

User = settings.AUTH_USER_MODEL

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120, null=True)
    handle = models.SlugField(null=True, blank=True, unique=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = unique_slugify(self, slug_field='handle')
        super().save(*args, **kwargs)