from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.app_tasks.models import Task, Comment
from apps.app_boards.models import Board
from .serializers import TaskSerializer, CommentSerializer
from .permissions import CanDeleteComment, CanDeleteTask, is_board_member


"""
    API endpoint for retrieving all tasks assigned to the authenticated user.
"""
class AssignedToMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

"""
    API endpoint for retrieving all tasks where the authenticated user is the reviewer.
"""
class ReviewingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

"""
    API endpoint for creating a new task.
    Requires the authenticated user to be a member of the selected board.
"""
class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        board_id = request.data.get("board")
        if not board_id:
            return Response({"error": "Board is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)
        if not is_board_member(request.user, board):
            return Response({"error": "You are not a member of this board"},status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        task = serializer.save(created_by=request.user)
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

"""
    API endpoint for updating or deleting a single task.
    PATCH:
    - Updates an existing task
    DELETE:
    - Deletes a task if the user is allowed to do so
"""
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if not is_board_member(request.user, task.board):
            return Response({"error": "You are not a member of this board"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        task = serializer.save()
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        permission = CanDeleteTask()
        if not permission.has_object_permission(request, self, task):
            return Response({"error": "You do not have permission to delete this task"}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

"""
    API endpoint for listing and creating comments for a task.
    GET:
    - Returns all comments for the selected task
    POST:
    - Creates a new comment for the selected task
"""
class TaskCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not is_board_member(request.user, task.board):
            return Response({"error": "You are not a member of this board"}, status=status.HTTP_403_FORBIDDEN)
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not is_board_member(request.user, task.board):
            return Response({"error": "You are not a member of this board"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save(task=task, author=request.user)
        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

"""
    API endpoint for deleting a single comment from a task.
    Only the author of the comment is allowed to delete it.
"""
class TaskCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, task_id=task_id)
        permission = CanDeleteComment()
        if not permission.has_object_permission(request, self, comment):
            return Response({"error": "You do not have permission to delete this comment"}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)