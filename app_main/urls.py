from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('users/', views.users_page, name='users'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('posts/', views.all_posts, name='all_posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('new-post/', views.post_create, name='post_create'),
    path('post-update/<int:post_id>/', views.post_update, name='post_update'),
    path('post-update/<int:post_id>/', views.post_update, name='post_update'),
    path('post-delete/<int:post_id>/', views.post_delete, name='post_delete'),
]