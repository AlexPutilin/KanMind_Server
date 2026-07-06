from django.contrib.auth.models import User
from rest_framework import serializers

"""
    Serializer for basic user information.
    Returns a simplified user representation including:
    - id
    - email
    - fullname (combined first and last name)
"""
class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"


"""
    Serializer for user registration.
    Handles:
    - Email uniqueness validation
    - Password validation and confirmation
    - Fullname validation (must include first and last name)
    - User creation with split fullname into first_name and last_name
"""
class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")
        if " " not in data["fullname"]:
            raise serializers.ValidationError("Enter full name (first and last name)")
        return data

    def create(self, validated_data):
        fullname = validated_data.pop("fullname")
        validated_data.pop("repeated_password")
        first_name, last_name = fullname.split(" ", 1)
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name
        )
        return user