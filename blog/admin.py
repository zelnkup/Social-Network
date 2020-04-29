from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth', 'photo']

# @admin.register(GeeksModel)
# class PostAdmin(admin.ModelAdmin):
# 	list_display = ['title', 'slug', 'content', 'created', 'updated']
# 	list_filter = ['created']
# 	prepopulated_fields = {'slug': ('title',)}
