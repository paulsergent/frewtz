from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer, UserUpdateSerializer
from .models import User
from rest_framework import status, permissions 
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import redirect, render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication




class UserViewRegister(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    
    def get(self, request):
        serializer = UserSerializer()
        return Response({'serializer': serializer})
    
    def post(self, request):
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        
        
        if not serializer.is_valid():
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        access = AccessToken.for_user(serializer.instance)
        user = serializer.instance
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user = authenticate(request, email=user.email, password=request.data.get('password'))
        response = Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        return response
    

class UserViewLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = UserLoginSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data.get('user')

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        response = Response({'access_token': access, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        return response
    
    
def user_profile(request):
    permission_classes = [permissions.IsAuthenticated]
    user = request.user
    if request.method == 'POST':
        serializer = UserUpdateSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_profile')
    else:
        serializer = UserUpdateSerializer(user)
    
    return render(request, 'users/profile.html', {'serializer': serializer})




class UserProfileUpdate(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response({'serializer': serializer})

    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'serializer': serializer}, status=status.HTTP_200_OK)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # if serializer.is_valid():
        #     updated_user = serializer.save()
        #     if serializer.validated_data.get('role') == 'farmer':
        #         from farmers.models import Farmer  # Import here to avoid circular import
        #         Farmer.objects.get_or_create(
        #             user=updated_user)
        #     return Response({'serializer': serializer}, status=status.HTTP_200_OK)
        # return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   
def user_profile_delete(request):
    permission_classes = [permissions.IsAuthenticated]
    if user := request.user:
        user.delete()
    return redirect('index')

def logout_user(request):
    
    logout(request)
    response = redirect('index')
    response.delete_cookie('access')  # Remove the access token cookie
    return response
    
    

    