from rest_framework.permissions import BasePermission


"""
    Helper function to check if a user has access to a board.
    Returns True if the user is:
    - the owner of the board
    - a member of the board
"""
def is_board_member(user, board):
    return user == board.owner or board.members.filter(id=user.id).exists()


"""
    Permission to allow access only if the user is a member of the task's board.
"""
class IsTaskBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return is_board_member(request.user, obj.board)


"""
    Permission to allow deletion of a task only if the user is:
    - the creator of the task
    - the owner of the board
"""
class CanDeleteTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by or request.user == obj.board.owner


"""
    Permission to allow deletion of a comment only by its author.
"""
class CanDeleteComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author