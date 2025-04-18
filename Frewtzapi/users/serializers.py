from rest_framework import serializers

from .models import User
from django.contrib.auth import authenticate




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=100, style={'input_type': 'password', 'placeholder': 'Password'})  # Make password write-only
    password_2 = serializers.CharField(write_only=True, max_length=100, style={'input_type': 'password', 'placeholder': 'Password'})
    class Meta:
        model = User
        fields = ['email', 'password', 'password_2']
        
    
    def validate(self, attrs):
        print(attrs, "FROM SERIALIZERS")
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        try:
            user = User(
                email=validated_data['email'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone_number=validated_data.get('phone_number', ''),
                role=validated_data.get('role', 'customer'),
            )
            user.set_password(validated_data['password'])  # Hash the password
            user.save()
            return user
        except Exception as e:
            print(e, "FROM SERIALIZERS")
            raise serializers.ValidationError("User could not be created.")
        
        


    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})
    class Meta:
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if user is None or password is None:
            raise serializers.ValidationError("Invalid email or password")
        if not user:
            raise serializers.ValidationError("User not found")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
       
       
        attrs['user'] = user
        return attrs
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'role']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'role': {'required': False}
        }
    
    
