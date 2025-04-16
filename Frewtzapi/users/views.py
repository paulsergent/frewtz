from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions 
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import redirect
from django.contrib.auth import get_user_model




class UserViewRegister(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/signup.html'
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
        if user is not None:
            
            login(request, user)
        response = redirect('index')
        response.set_cookie('access', str(access), httponly=True)
        return response
    

class UserViewLogin(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/login.html'
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

        response = redirect('index')
        response.set_cookie(
            'access_token', 
            access, 
            httponly=True,
            max_age=60*60*24,  # 1 day)
        )
        response.set_cookie(
            'refresh_token', str(refresh),
            httponly=True,
            max_age=60*60*24*7,  # 7 days)
        )
        return response
    
    
    
    
    

def logout_user(request):
    
    logout(request)
    response = redirect('index')
    response.delete_cookie('access')  # Remove the access token cookie
    return response
    
    

    