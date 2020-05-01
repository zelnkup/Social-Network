from django.contrib.auth.models import User
import random

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


def image_folder():
	return


class PublishedManager(models.Manager):

	def get_queryset(self):
		return super(PublishedManager, self).get_queryset() \
			.filter(status='published')


def gen_token():
	symbols = 'ab1cd2ef3gh4ij5kl6mn7op8qr9stuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM'
	post_id = ''.join([random.choice(symbols) for i in range(10)])
	return post_id


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=False)
	body = models.TextField()
	token = models.CharField(max_length=10, default=gen_token, unique=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	objects = models.Manager()  # The default manager.
	published = PublishedManager()  # Our custom manager.

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail',
					   args=[self.publish.year,
							 self.publish.month,
							 self.publish.day,
							 self.slug,
							 self.token])
