from rest_framework import serializers, status
from rest_framework.response import Response
from .models import User





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # or specify the fields you want to include

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.create(user=user, **validated_data)
        return product
    
    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'POST':
            fields.pop('id', None)
        return fields
    


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance