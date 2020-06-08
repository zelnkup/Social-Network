from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		widgets = {
			'body': SummernoteWidget(),
		}
		fields = ['title','preview', 'body', 'status']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content',]