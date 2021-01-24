from django.urls import path
from .views import (
    StatusIndexView,
)

app_name = 'statuses'

urlpatterns = [
    path('statuses/', StatusIndexView.as_view(), name='index'),
]
