import random

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from uuslug import uuslug


def image_folder():
    return


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


def gen_token():
    symbols = "ab1cd2ef3gh4ij5kl6mn7op8qr9stuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM"
    post_id = "".join([random.choice(symbols) for i in range(10)])
    return post_id


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, unique=False
    )
    body = models.TextField()
    preview = models.ImageField(upload_to="images", blank=True)
    token = models.CharField(max_length=10, default=gen_token, unique=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.token])

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="commented_post"
    )
    content = models.TextField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.content
