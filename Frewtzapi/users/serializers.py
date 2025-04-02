from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
        read_only_fields = ('id', 'is_active', 'is_staff')

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        role = attrs.get('role')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        if role and user.role != role:
            raise serializers.ValidationError("Invalid role")
        return {'email': email, 'password': password, 'role': role}
    
    
