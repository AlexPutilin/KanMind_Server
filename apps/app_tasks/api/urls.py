from django.urls import path
from .views import (AssignedToMeView, ReviewingView, TaskCommentsView, TaskCommentDetailView, TaskCreateView, TaskDetailView)

urlpatterns = [
    path("", TaskCreateView.as_view()),
    path("assigned-to-me/", AssignedToMeView.as_view()),
    path("reviewing/", ReviewingView.as_view()),
    path("<int:pk>/", TaskDetailView.as_view()),
    path("<int:task_id>/comments/", TaskCommentsView.as_view()),
    path("<int:task_id>/comments/<int:comment_id>/", TaskCommentDetailView.as_view()),
]