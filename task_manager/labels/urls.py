from django.urls import path
from .views import (
    LabelIndexView,
    LabelCreateView,
    LabelUpdateView,
)

app_name = 'labels'

urlpatterns = [
    path('labels/', LabelIndexView.as_view(), name='index'),
    path('labels/create/', LabelCreateView.as_view(), name='create'),
    path('labels/<int:pk>/update/', LabelUpdateView.as_view(), name='update'),
]
