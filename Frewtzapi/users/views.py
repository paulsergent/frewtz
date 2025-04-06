from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken



class UserViewRegister(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Implement your user registration logic here
        # For example, you can create a new user using the User model
        # and return a success response.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None :
            return Response({"message": "Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)
        # Implement your user login logic here
        # For example, you can authenticate the user and return a success response.
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        #generate JWT token
        access = AccessToken.for_user(user)
        return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
