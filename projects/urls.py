from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/new/', views.project_create, name='project-create'),
    path('project/<slug:slug>/', views.project_details, name='project-details'),
    path('project/update/<slug:slug>/', views.project_update, name='project-update'),
    path('project/delete/<slug:slug>/', views.project_delete, name='project-delete'),
]
