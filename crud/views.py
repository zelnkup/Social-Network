from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView

from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.core.paginator import Paginator


class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'crud/list.html'

	def get_queryset(self):
		queryset = {'all_posts': Post.published.all().order_by('-created'),
					'popular_posts': Post.published.all().order_by('-views')[:5]}
		return queryset


# class PopularPostListView(ListView):
# 	queryset = Post.published.all().order_by('views')
# 	context_object_name = 'popular_posts'
# 	template_name = 'crud/list.html'


@login_required
def post_detail(request, year, month, day, slug, token):
	post = get_object_or_404(Post, slug=slug, token=token,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)
	post.views += 1
	post.save()
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			form.instance.post = post
			form.instance.user = request.user
			form.save()
			form = CommentForm()
			messages.success(request, 'Comment added')
	else:
		form = CommentForm()
	comments = Comment.objects.filter(post=post).order_by('-created_at')

	return render(request, 'crud/post_detail.html',
				  {
					  'post': post,
					  'form': form,
					  'comments': comments,
				  })


@login_required
def create_view(request):
	# add the dictionary during initialization
	if request.method == "POST":
		form = PostForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save(commit=False)
			form.instance.user = request.user
			value = form.instance.title
			form.instance.slug = slugify(value, allow_unicode=True)
			form.save()
			messages.success(request, 'Post added')
			return redirect('/')
		else:
			messages.error(request, 'Error adding your post')
	else:
		form = PostForm()

	return render(request, "create_view.html", {'form': form})


@login_required
def delete_view(request, token):
	post = Post.objects.get(token=token)
	if request.user == post.user:
		post.delete()

	return redirect('/')
