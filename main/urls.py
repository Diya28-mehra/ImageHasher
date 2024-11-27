from django.urls import path
from .views import (
    ImageListCreateAPIView,
    ImageRetrieveUpdateAPIView,
    ImageDeleteAPIView,
)

urlpatterns = [
    path('images/', ImageListCreateAPIView.as_view(), name='image-list'),
    path('images/<int:pk>/', ImageRetrieveUpdateAPIView.as_view(), name='image-detail'),
    path('images/<int:pk>/delete/', ImageDeleteAPIView.as_view(), name='image-delete'),
]
