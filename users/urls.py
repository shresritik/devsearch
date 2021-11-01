from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('account/', views.accountUser, name="account"),
    path('edit-profile/', views.editAccount, name="edit-profile"),
    path('logout/', views.logoutUser, name="logout"),
    path('inbox/', views.inbox, name="inbox"),
    path('create-skill/', views.createSkill, name="create-skill"),
    path('update-skill/<str:pk>/', views.updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.deleteSkill, name="delete-skill"),
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),

]
