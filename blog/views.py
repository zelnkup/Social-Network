from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import UserEditForm, ProfileEditForm


@login_required
def dashboard(request):
	return render(request,
				  'blog/dashboard.html',
				  {'section': 'dashboard'})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,
								 data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated ' \
									  'successfully')
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
	return render(request, 'user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	return render(request, 'user/detail.html', {'section': 'people', 'user': user})
