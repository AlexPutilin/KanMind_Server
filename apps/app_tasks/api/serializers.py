from django.contrib.auth.models import User
from rest_framework import serializers
from apps.app_auth.api.serializers import UserSerializer
from apps.app_tasks.models import Task, Comment


"""
    Serializer for creating, updating, and retrieving tasks.
    Handles:
    - Task data including status, priority, and due date
    - Assignment of assignee and reviewer via user IDs
    - Validation of board membership for assignee and reviewer
    - Preventing changes to the assigned board after creation
    - Returning the number of related comments
"""
class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="assignee", write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="reviewer", write_only=True, required=False, allow_null=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "assignee_id",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value
    
    def validate(self, data):
        board = data.get("board")
        if self.instance:
            if "board" in data and data["board"] != self.instance.board:
                raise serializers.ValidationError("Board cannot be changed")
            board = self.instance.board
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")
        if self.instance and "assignee" not in data:
            assignee = self.instance.assignee
        if self.instance and "reviewer" not in data:
            reviewer = self.instance.reviewer
        if assignee and not board.members.filter(id=assignee.id).exists():
            raise serializers.ValidationError("Assignee must be a member of this board")
        if reviewer and not board.members.filter(id=reviewer.id).exists():
            raise serializers.ValidationError("Reviewer must be a member of this board")
        return data

    def get_comments_count(self, obj):
        return obj.comments.count()


"""
    Serializer for creating and retrieving task comments.
    Handles:
    - Comment content validation
    - Returning author fullname instead of raw user data
"""
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Content cannot be empty")
        return value

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"