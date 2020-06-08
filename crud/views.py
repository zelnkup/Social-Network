from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView

from .forms import PostForm, CommentForm
from .models import Post, Comment


def post_list(request):
    posts = Post.published.all().order_by('-created')

    popular_posts = Post.published.all().order_by('-views')[:5]

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'base.html', {'popular_posts': popular_posts,
                                         'posts': posts})


def post_detail(request, token):
    post = get_object_or_404(Post, token=token,
                             )
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
    popular_posts = Post.published.all().order_by('-views')[:5]
    return render(request, 'crud/post_detail.html',
                  {
                      'post': post,
                      'form': form,
                      'comments': comments,
                      'popular_posts': popular_posts
                  })


@login_required
def create_view(request):
    # add the dictionary during initialization
    popular_posts = Post.published.all().order_by('-views')[:5]
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Post added')
            return redirect('/')
        else:
            messages.error(request, 'Error adding your post')
    else:
        form = PostForm()

    return render(request, "create_view.html", {'form': form, 'popular_posts': popular_posts})


@login_required
def delete_view(request, token):
    post = Post.objects.get(token=token)
    if request.user == post.user:
        post.delete()

    return redirect('/')


class PostUpdate(UpdateView):
    model = Post
#	fields = ['title', 'body', 'preview', 'status', ]
    form_class = PostForm

    def get_object(self, *args, **kwargs):
        post = super(PostUpdate, self).get_object(*args, **kwargs)
        if post.user != self.request.user:
            raise PermissionDenied()  # or Http404
        return post
