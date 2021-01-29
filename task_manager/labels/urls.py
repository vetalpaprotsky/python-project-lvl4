from django.urls import path
from .views import (
    LabelIndexView,
)

app_name = 'labels'

urlpatterns = [
    path('labels/', LabelIndexView.as_view(), name='index'),
]
