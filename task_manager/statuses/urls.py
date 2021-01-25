from django.urls import path
from .views import (
    StatusIndexView,
    StatusCreateView,
    StatusUpdateView,
)

app_name = 'statuses'

urlpatterns = [
    path('statuses/', StatusIndexView.as_view(), name='index'),
    path('statuses/create/', StatusCreateView.as_view(), name='create'),
    path(
        'statuses/<int:pk>/update/', StatusUpdateView.as_view(), name='update'
    ),
]
