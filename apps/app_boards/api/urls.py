from django.urls import path
from .views import BoardDetailView, BoardListCreateView


urlpatterns = [
    path("", BoardListCreateView.as_view()),
    path("<int:pk>/", BoardDetailView.as_view()),
]