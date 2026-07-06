from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.app_boards.models import Board
from apps.app_auth.api.serializers import UserSerializer
from .serializers import BoardListSerializer, BoardDetailSerializer, BoardUpdateSerializer
from .permissions import is_board_member


"""
    API endpoint for listing and creating boards.
    GET:
    - Returns all boards where the authenticated user is owner or member
    POST:
    - Creates a new board with the authenticated user as owner
    - Allows adding members to the board
"""
class BoardListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct()
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardListSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        board = serializer.save()
        response_serializer = BoardListSerializer(board)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

"""
    API endpoint for retrieving, updating, and deleting a single board.
    GET:
    - Returns board details including members and tasks
    PATCH:
    - Updates board title and members
    DELETE:
    - Deletes the board (only allowed for the owner)
"""
class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Board, pk=pk)

    def get(self, request, pk):
        board = self.get_object(pk)
        if not is_board_member(request.user, board):
            return Response({"error": "You do not have permission to view this board"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        board = self.get_object(pk)
        if not is_board_member(request.user, board):
            return Response({"error": "You do not have permission to edit this board"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BoardUpdateSerializer(board, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        board = serializer.save()
        response_serializer = BoardUpdateSerializer(board)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        board = self.get_object(pk)
        if request.user != board.owner:
            return Response({"error": "Only the owner can delete this board"}, status=status.HTTP_403_FORBIDDEN)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

"""
    API endpoint for checking if a user email exists.
    GET:
    - Expects an email as query parameter
    - Returns user information if email exists
    - Returns 404 if no user is found
"""
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)