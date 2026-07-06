from django.db import models
from django.contrib.auth.models import User
from apps.app_boards.models import Board


"""
    Model representing a task within a board.
    A task belongs to a board and includes:
    - title and description
    - status and priority
    - optional assignee and reviewer
    - due date
    - creator of the task
"""
class Task(models.Model):
    status_choices = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]

    priority_choices = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default="to-do")
    priority = models.CharField(max_length=10, choices=priority_choices, default="medium")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_tasks")
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")

    def __str__(self):
        return self.title
    

"""
    Model representing a comment on a task.
    A comment is linked to a task and includes:
    - the author
    - the content of the comment
    - the creation timestamp
"""
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment {self.id} on task {self.task_id}"