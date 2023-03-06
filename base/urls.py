from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.base_home, name='base-home'),
    path('inbox/', views.inbox_page, name='inbox'),
    path('message/<str:pk>/', views.message_page, name='message'),
    path('reply/<str:pk>/', views.message_reply, name='message-reply'),
]
