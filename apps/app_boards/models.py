from django.db import models
from django.contrib.auth.models import User


"""
    Model representing a Kanban board.
    A board has:
    - a title
    - an owner (creator of the board)
    - multiple members who have access to the board
"""
class Board(models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_boards")
    members = models.ManyToManyField(User, related_name="boards")

    def __str__(self):
        return self.title