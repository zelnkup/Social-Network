from django.urls import path

from . import views

urlpatterns = [

	path('edit/', views.edit, name='edit'),
	path('users/', views.user_list, name='user_list'),
	path('users/<username>/', views.user_detail, name='user_detail'),

]
