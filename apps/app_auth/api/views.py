from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer


"""
    API endpoint for user registration.
    Creates a new user account and returns:
    - authentication token
    - user email
    - full name
    - user id
"""
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            response_data = {
                "token": token.key, 
                "fullname": f"{user.first_name} {user.last_name}", 
                "email": user.email,
                "user_id": user.pk
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

"""
    API endpoint for user login.
    Authenticates a user using email and password
    and returns:
    - authentication token
    - user email
    - full name
    - user id
"""
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            token = Token.objects.get(user=user)
            response_data = {
                "token": token.key, 
                "fullname": f"{user.first_name} {user.last_name}", 
                "email": user.email,
                "user_id": user.pk
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)