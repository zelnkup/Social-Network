from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('date_of_birth', 'photo')


class SignupForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ()

	def signup(self, request, user):
		user.save()
		Profile.objects.create(user=user)

# class GeeksForm(forms.ModelForm):
# 	# create meta class
# 	class Meta:
# 		# specify model to be used
# 		model = GeeksModel
#
# 		# specify fields to be used
# 		fields = [
# 			"title",
# 			"content",
# 		]
