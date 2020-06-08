from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
	list_display = ('title', 'status', 'user', 'publish', 'created', 'updated')
	list_filter = ('status', 'created', 'publish', 'user')
	search_fields = ('title', 'body')
	summernote_fields = ('body',)



admin.site.register(Comment)
