from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .forms import PostCreate
from django.db.models import F

from .models import Post


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'crud/list.html'

# class UserPostListView(ListView):
# 	queryset = Post.objects.filter(author=F('title'))
# 	context_object_name = 'userposts'
# 	paginate_by = 3
# 	template_name = 'user/detail.html'

# def post_list(request):
# 	object_list = Post.published.all()
# 	paginator = Paginator(object_list, 3)  # 3 posts in each page
# 	page = request.GET.get('page')
# 	try:
# 		posts = paginator.page(page)
# 	except PageNotAnInteger:
# 		# If page is not an integer deliver the first page
# 		posts = paginator.page(1)
# 	except EmptyPage:
# 		# If page is out of range deliver last page of results
# 		posts = paginator.page(paginator.num_pages)
# 	return render(request, 'blog/list.html',
# 				  {
# 					  'posts': posts,
# 					  'page': page,
# 				  })


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)
	return render(request, 'crud/post_detail.html',
				  {
					  'post': post
				  })

