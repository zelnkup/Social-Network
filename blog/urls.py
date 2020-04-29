from django.urls import path

from . import views

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('edit/', views.edit, name='edit'),
	path('users/', views.user_list, name='user_list'),
	path('users/<username>/', views.user_detail, name='user_detail'),

	# path('', views.PostListView.as_view(), name='post_list'),
	# path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
	# path('post/new/', views.create_view, name='create_post'),
	# path('post/<int:id>/<slug:slug>/', views.post_detail, name='post_detail'),
]
