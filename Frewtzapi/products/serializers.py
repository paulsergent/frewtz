from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Product
from users.models import User





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'thumbnail']  # or specify the fields you want to include

    def create(self, validated_data):
        farmer = self.context['request'].user.farmer_user
        name = validated_data.get('name')
        if not name:
            raise serializers.ValidationError("Product name is required.")
        slug = name.replace(" ", "-").lower()
        if Product.objects.filter(slug=slug).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        product = Product.objects.create(farmer=farmer, slug=slug, **validated_data)
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
        instance.stock = validated_data.get('stock', instance.stock)
        if 'thumbnail' in validated_data:
            instance.thumbnail = validated_data['thumbnail']
        instance.save()
        return instance