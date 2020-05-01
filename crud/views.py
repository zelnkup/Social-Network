from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView
from django.utils.text import slugify

from .forms import PostForm
from .models import Post


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'crud/list.html'


@login_required
def post_detail(request, year, month, day, slug,token):
	post = get_object_or_404(Post, slug=slug, token=token,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)
	return render(request, 'crud/post_detail.html',
				  {
					  'post': post
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


