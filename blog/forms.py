from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django import forms
from django.contrib.auth.models import User

from .models import Profile


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
	class Meta:
		model = Profile
		fields = ()


	def save_user(self, request, sociallogin, form):
		user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)
		Profile.objects.create(user=user)

		return user


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

# class MyCustomSocialSignupForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ()
#
# 	def save(self):
# 		# Ensure you call the parent class's save.
# 		# .save() returns a User object.
# 		user = super(MyCustomSocialSignupForm, self).save()
# 		Profile.objects.create(user=user)
# 		# Add your own processing here.
#
# 		# You must return the original result.
# 		return user

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
