from django.urls import path
from .views import (
    IndexView,
    CreateView,
    UpdateView,
    delete,
    LoginView,
    LogoutView,
)

app_name = 'users'

urlpatterns = [
    path('users/', IndexView.as_view(), name='index'),
    path('users/create/', CreateView.as_view(), name='create'),
    path('users/<int:pk>/update/', UpdateView.as_view(), name='update'),
    path('users/<int:pk>/delete/', delete, name='delete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
