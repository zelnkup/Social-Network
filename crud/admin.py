from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'author', 'publish')
	list_filter = ('status', 'created', 'publish', 'author')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	# raw_id_fields = ('author',)
	# date_hierarchy = 'published_at'
	# ordering = ('available', 'published_at')
