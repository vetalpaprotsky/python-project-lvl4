from django.urls import path
from .views import (
    LabelIndexView,
    LabelCreateView,
)

app_name = 'labels'

urlpatterns = [
    path('labels/', LabelIndexView.as_view(), name='index'),
    path('labels/create/', LabelCreateView.as_view(), name='create'),
]
