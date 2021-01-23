from django.urls import path
from .views import (
    UserIndexView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserLoginView,
    UserLogoutView,
)

app_name = 'users'

urlpatterns = [
    path('users/', UserIndexView.as_view(), name='index'),
    path('users/create/', UserCreateView.as_view(), name='create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
