from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import UserEditForm, ProfileEditForm
from crud.models import Post
from django.db.models import F

@login_required
def dashboard(request):
	return render(request, 'blog/dashboard.html', )


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,
								 data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request,
				  'blog/edit.html',
				  {'user_form': user_form,
				   'profile_form': profile_form})


@login_required
def user_list(request):
	users = User.objects.filter(is_active=True)
	return render(request, 'user/list.html', {'users': users,
											  })


@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	posts = Post.published.filter(author=user)
	# posts = Post.published.all()
	return render(request, 'user/detail.html', {'user': user,
												'posts': posts})

# @login_required
# def create_view(request):
# 	# add the dictionary during initialization
# 	if request.method == "POST":
# 		form = GeeksForm(request.POST)
# 		if form.is_valid():
# 			post = form.save(commit=False)
# 			post.user = request.user
# 			post.save()
# 			return redirect('/')
# 	else:
# 		form = GeeksForm()
#
# 	return render(request, "create_view.html", {'form': form})


# @login_required
# def post_list(request):
# 	posts = GeeksModel.objects.all()
# 	return render(request, 'post_list.html', {'posts': posts})
#
#
# @login_required
# def post_detail(request, id, slug):
# 	post = get_object_or_404(GeeksModel, id=id, slug=slug)
# 	return render(request, 'post_detail.html', {'post': post})
