from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('projects/<str:pk>/', views.project, name="project"),
    path('create-form/', views.createForm, name="create-form"),
    path('update-form/<str:pk>', views.updateForm, name="update-form"),
    path('delete-form/<str:pk>', views.deleteForm, name="delete-form"),
]
