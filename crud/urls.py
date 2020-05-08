from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
app_name = 'blog'
urlpatterns = [
	# post views
	#	path('', views.post_list, name='post_list'),
	path('', login_required(views.PostListView.as_view()), name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:slug>/<str:token>', views.post_detail, name='post_detail'),
	path('post/new', views.create_view, name='create_post'),
	path('delete/<str:token>', views.delete_view, name='delete_post'),
	# path('<int:year>/<int:month>/<int:day>/<slug:slug>/<str:token>/', views.OrderCreate, name='OrderCreate'),
]
