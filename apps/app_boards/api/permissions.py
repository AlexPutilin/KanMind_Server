from rest_framework.permissions import BasePermission


"""
    Helper function to check if a user has access to a board.
    Returns True if the user is:
    - the owner of the board
    - a member of the board
"""
def is_board_member(user, board):
    return user == board.owner or board.members.filter(id=user.id).exists()