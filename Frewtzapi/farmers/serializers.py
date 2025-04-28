from rest_framework import serializers
from .models import Farmer



class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['farm_name', 'farm_location', 'farm_description', 'profile_picture']
        extra_kwargs = {
            'farm_name': {'required': True},
            'farm_location': {'required': True},
            'farm_description': {'required': False},
            'profile_picture': {'required': False}
        }
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # Remove 'user' if present
        farmer = Farmer.objects.create(user=user, **validated_data)
        return farmer

