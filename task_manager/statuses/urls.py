from django.urls import path
from .views import (
    StatusIndexView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
)

app_name = 'statuses'

urlpatterns = [
    path('statuses/', StatusIndexView.as_view(), name='index'),
    path('statuses/create/', StatusCreateView.as_view(), name='create'),
    path(
        'statuses/<int:pk>/update/', StatusUpdateView.as_view(), name='update'
    ),
    path(
        'statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name='delete'
    ),
]
