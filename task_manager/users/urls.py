from django.urls import path
from .views import IndexView, create, update, LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    path('users/', IndexView.as_view(), name='index'),
    path('users/create/', create, name='create'),
    path('users/<int:pk>/update/', update, name='update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
