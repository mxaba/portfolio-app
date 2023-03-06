from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('post/new/', views.post_create, name='post-create'),
    path('user/<str:username>/', views.user_posts, name='user-posts'),
    path('post/<slug:slug>/', views.post_details, name='post-details'),
    path('post/update/<slug:slug>/', views.post_update, name='post-update'),
    path('post/delete/<slug:slug>/', views.post_delete, name='post-delete'),
]
