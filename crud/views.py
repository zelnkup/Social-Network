from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView
from django.contrib import messages

from .forms import PostForm, CommentForm
from .models import Post,Comment


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'crud/list.html'


@login_required
def post_detail(request, year, month, day, slug, token):
	post = get_object_or_404(Post, slug=slug, token=token,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			form.instance.post = post
			form.instance.user = request.user
			form.save()
			messages.success(request, 'Comment added')
	else:
		form = CommentForm()
	comments=Comment.objects.filter(post = post).order_by('-created_at')

	return render(request, 'crud/post_detail.html',
				  {
					  'post': post,
					  'form': form,
					  'comments':comments,
				  })


@login_required
def create_view(request):
	# add the dictionary during initialization
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			form.instance.user = request.user
			value = form.instance.title
			form.instance.slug = slugify(value, allow_unicode=True)
			form.save()
			return redirect('/')
	else:
		form = PostForm()

	return render(request, "create_view.html", {'form': form})


@login_required
def delete_view(request, token):
	post = Post.objects.get(token=token)
	if request.user == post.user:
		post.delete()

	return redirect('/')
