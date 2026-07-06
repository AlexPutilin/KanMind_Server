from django.contrib.auth.models import User
from rest_framework import serializers
from apps.app_auth.api.serializers import UserSerializer
from apps.app_tasks.api.serializers import TaskSerializer
from apps.app_boards.models import Board


"""
    Serializer for listing and creating boards.
    Handles:
    - Board creation with owner and members
    - Aggregated fields like member count and task statistics
    - Validation of board title
"""
class BoardListSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, required=False)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        user = self.context["request"].user
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set(members)
        return board

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()
    

"""
    Serializer for retrieving a single board with full details.
    Includes:
    - Board information
    - Member data
    - All related tasks
"""
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        ]


"""
    Serializer for updating board title and members.
    Handles:
    - Updating board title
    - Adding or removing members
    - Returning detailed owner and member data
"""
class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    owner_data = UserSerializer(source="owner", read_only=True)
    members_data = UserSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "owner_data",
            "members_data",
        ]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value

    def update(self, instance, validated_data):
        members = validated_data.pop("members", None)
        if "title" in validated_data:
            instance.title = validated_data["title"]
            instance.save()
        if members is not None:
            instance.members.set(members)
        return instance