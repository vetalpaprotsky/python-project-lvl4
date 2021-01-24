from django.urls import path
from .views import (
    StatusIndexView,
    StatusCreateView,
)

app_name = 'statuses'

urlpatterns = [
    path('statuses/', StatusIndexView.as_view(), name='index'),
    path('statuses/create/', StatusCreateView.as_view(), name='create'),
]
